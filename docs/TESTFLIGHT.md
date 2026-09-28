# TestFlight release

App Store Connect record: [Leetcode on the go](https://appstoreconnect.apple.com/apps/6816836452/testflight/ios).

Release builds use `com.ethanrimes.leetcode-on-the-go`, version `1.0`, based on the app record and SKU shown by the owner. Confirm the full Bundle ID in App Information before the first upload. Debug builds retain `com.ethanrimes.patternatlas`, so existing simulator progress and the history import script continue to work.

The app includes the 1024×1024 opaque icon, a UserDefaults required-reason privacy declaration (`CA92.1`), all iPad orientations, and the existing exempt-encryption declaration. The privacy manifest describes required-reason API access; it does not replace the App Store Connect privacy questionnaire. Optional Azure sync sends the user's LeetCode account and submission history to their configured private backend. Personal history and sync credentials are not bundled in the app.

## GitHub Actions delivery (preferred)

The [TestFlight workflow](../.github/workflows/ios-testflight.yml) follows AgroAmigo's distribution approach: native checks first, a temporary keychain on a GitHub macOS runner, manual App Store signing, then an API-key upload with `altool`. This app remains SwiftUI; Flutter and CocoaPods are not needed. Local Xcode Apple-account sign-in is not required for this route.

The owner-provided `ios dev` folder has a matching App Store Connect API key and issuer ID, a distribution certificate/private key, and a working P12 password. Its embedded provisioning profile and `IOS_BUNDLE_ID` belong to Money Control. The setup script deliberately uses this repository's bundle ID and never uploads that mismatched profile.

From the repository root, run these once in a terminal with access to Apple and GitHub:

```sh
npm run ios:signing:inspect -- '../ios dev'
npm run ios:signing:configure -- '../ios dev'
git push origin main
```

`inspect` is offline and outputs only validation results. `configure` verifies the existing App Store Connect app's bundle ID, finds the matching certificate and a current App Store profile, or creates a profile for this app. It then configures the following encrypted secrets **only** in `ethanrimes/leetcode-on-the-go`: `APPLE_TEAM_ID`, `BUILD_CERTIFICATE_BASE64`, `P12_PASSWORD`, `BUILD_PROVISION_PROFILE_BASE64`, `APP_STORE_CONNECT_API_KEY_ID`, `APP_STORE_CONNECT_API_KEY_ISSUER_ID`, and `APP_STORE_CONNECT_API_KEY_BASE64`. It does not edit the source credential folder or other apps. The API key needs access to the app and to Certificates, Identifiers & Profiles; `gh` must be signed in with repository-secret administration permission.

The workflow runs for iOS/content changes pushed to `main`, or manually:

```sh
gh workflow run ios-testflight.yml --repo ethanrimes/leetcode-on-the-go --ref main
gh run list --repo ethanrimes/leetcode-on-the-go --workflow ios-testflight.yml
```

Version remains `1.0`; build numbers use the workflow run number and attempt (`1.1`, `2.1`, `2.2`, etc.). The workflow checks the exact profile app/team, certificate membership, expiry, and App Store distribution type before installing it. Signing files and the temporary keychain are removed afterward; IPA and symbols are retained as GitHub artifacts for one day. A successful upload is separate from Apple processing and TestFlight tester assignment.

## Local Xcode alternative

Sign in to the paid Apple Developer account in **Xcode → Settings → Accounts**. Confirm the development team and the next unused build number in App Store Connect. Run from the repository root in a local terminal with Xcode, Apple network access, and Keychain access:

```sh
npm run ios:generate
export ATLAS_APPLE_TEAM_ID='YOUR_TEAM_ID'
export ATLAS_IOS_BUILD_NUMBER='1'
mkdir -p .local/releases
xcodebuild archive \
  -project apps/ios/PatternAtlas.xcodeproj \
  -scheme PatternAtlas -configuration Release \
  -destination 'generic/platform=iOS' \
  -archivePath ".local/releases/PatternAtlas-${ATLAS_IOS_BUILD_NUMBER}.xcarchive" \
  -derivedDataPath .local/releases/DerivedData \
  -allowProvisioningUpdates \
  DEVELOPMENT_TEAM="$ATLAS_APPLE_TEAM_ID" \
  CURRENT_PROJECT_VERSION="$ATLAS_IOS_BUILD_NUMBER"
xcodebuild -exportArchive \
  -archivePath ".local/releases/PatternAtlas-${ATLAS_IOS_BUILD_NUMBER}.xcarchive" \
  -exportOptionsPlist apps/ios/ExportOptions.plist \
  -exportPath ".local/releases/export-${ATLAS_IOS_BUILD_NUMBER}" \
  -allowProvisioningUpdates
```

The export command **uploads** to App Store Connect. Alternatively, choose the paid team under Signing & Capabilities, select Any iOS Device, use **Product → Archive**, then **Distribute App → App Store Connect** in Xcode. Keep the team in `project.yml` if it is saved in the generated project, or continue passing it at build time. Never commit signing credentials or private history.

Wait for Apple's processing to complete and inspect the build under TestFlight. Confirm the version, build number, and processing status; then assign the build to the intended internal testing group. External testing additionally requires Apple's beta review. An archive or successful upload alone does not establish tester availability.

## Preparation evidence · 2026-09-27

- XcodeGen regeneration and validation of Info.plist, PrivacyInfo.xcprivacy, and ExportOptions.plist passed.
- The icon is 1024×1024 with no alpha channel. The privacy manifest is included in the generated target's resource phase.
- Device archiving was attempted with signing disabled for a build check. It failed at asset compilation because the restricted process could not connect to CoreSimulatorService. No successful archive or upload was produced.
- The session found no Xcode Apple accounts, valid signing identities, or provisioning profiles. Computer Use denied access to both Xcode and Comet. Signing, account verification, Apple validation, and TestFlight processing remain unverified.

### Credential-folder and CI follow-up

- The owner subsequently signed in to Xcode; the local account inventory now contains one account. The CI route uses the API key instead.
- Offline checks confirmed matching API-key copies, the P12 password and private-key bag, matching distribution certificates, and certificate validity through May 14, 2027. The embedded profile targets `com.ethankallett.moneycontrol`, so it cannot sign Pattern Atlas.
- All seven credential-parser/profile-validation tests and Actionlint checks passed. This does not validate live Apple API permissions or prove a signed archive/upload.
- The restricted session cannot resolve Apple/GitHub hosts or access the local simulator service during archiving. No repository secrets have been uploaded, no Apple provisioning profile has been created, and no TestFlight build has been submitted from this session.

Apple references: [upload builds](https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds), [required-reason APIs](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api), and [iPad orientation support](https://developer.apple.com/documentation/uikit/uiviewcontroller/supportedinterfaceorientations).
