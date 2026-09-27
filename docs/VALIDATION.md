# Verification evidence

Verified on 2026-09-27. These results describe observed checks, not a guarantee that every algorithm passes LeetCode's private judge.

| Check | Observed result |
| --- | --- |
| Production web build | Passed TypeScript and Vite production compilation |
| Curriculum integrity | 704 nodes: 12 roots, 200 authored patterns, 313 source practice collections, 2,909 problems with solutions; references, hierarchy, and bundled web/iOS parity passed |
| Community integrity | 2,716 additional cards passed Python syntax, source SHA-256, attribution, and membership checks; imported code was not executed |
| Authored solution examples | All 200 pattern examples passed |
| Seeded algorithm checks | 1,355 differential/property checks passed, covering prefix counting, subarray/window methods, monotonic structures, string algorithms, range queries, lazy propagation, SCCs, and LFU eviction |
| Shared study logic | 7 tests passed for scheduling, filtered queues, backup validation/merge, collection membership, and sorting |
| Local browser flows | 16 Playwright tests passed across desktop and mobile viewports |
| Deployed browser flows | The same 16 Playwright tests passed against the Azure production URL |
| Native iOS | 7 tests passed on iPhone 17 Pro Simulator, iOS 26.1: 5 model/content/storage/scheduling tests and 2 UI tests exercising authored review and community search/reveal/attribution |
| Azure content | HTTPS returned 200; hosted curriculum matched the repository content byte for byte |

Live deployment: [Pattern Atlas](https://blue-sea-0c03ac51e.3.azurestaticapps.net).

The browser flows exercise four-level category navigation, solution reveal, draft persistence after reload, bookmarks, recall ratings, hidden answers in review, catalog search, official execution links, backup validation/merge, responsive navigation, and horizontal overflow. Native tests include decoding the expanded offline curriculum, numeric sorting, community attribution, persistence, and the portable backup format.

Visual inspection covered the desktop and mobile web layout and the native simulator home screen. The web editor is loaded separately from the initial page, and the Graphite theme uses system fonts.

## Reproduce

```sh
npm ci
npm run build
npm test
npx playwright install chromium
npm run test:e2e
ATLAS_TEST_URL=https://blue-sea-0c03ac51e.3.azurestaticapps.net npm run test:e2e
npm run ios:generate
xcodebuild test -project apps/ios/PatternAtlas.xcodeproj -scheme PatternAtlas \
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro' CODE_SIGNING_ALLOWED=NO
```

Use an available simulator name on your own machine. The GitHub iOS workflow selects an available iPhone automatically.

## Boundaries

- Authored examples and selected differential checks do not replace LeetCode's complete test suites. The application intentionally delegates code execution to LeetCode.
- Native physical-device signing, TestFlight, and App Store submission have not been performed.
- Progress is local to each device, with explicit JSON export/import; automatic cloud synchronization is not implemented.
- The reference catalog is larger than the set of worked cards. The [coverage audit](COVERAGE.md) lists rare specialist extensions and non-algorithm topics outside the current worked curriculum.
- GitHub Actions runs web validation before deployment. Individual workflow results are available in the repository's Actions tab.
