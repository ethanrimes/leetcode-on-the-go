# TestFlight release

App Store Connect record: [Leetcode on the go](https://appstoreconnect.apple.com/apps/6816836452/testflight/ios).

Release builds use `com.ethanrimes.leetcode-on-the-go`, version `1.0`, based on the app record and SKU shown by the owner. Confirm the full Bundle ID in App Information before the first upload. Debug builds retain `com.ethanrimes.patternatlas`, so existing simulator progress and the history import script continue to work.

The app includes the 1024×1024 opaque icon, a UserDefaults required-reason privacy declaration (`CA92.1`), all iPad orientations, and the existing exempt-encryption declaration. The privacy manifest describes required-reason API access; it does not replace the App Store Connect privacy questionnaire. Optional Azure sync sends the user's LeetCode account and submission history to their configured private backend. Personal history and sync credentials are not bundled in the app.

## Sign, archive, upload

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

Apple references: [upload builds](https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds), [required-reason APIs](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api), and [iPad orientation support](https://developer.apple.com/documentation/uikit/uiviewcontroller/supportedinterfaceorientations).
