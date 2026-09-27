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

## Progress dashboard update · 2026-09-27

- Web production build passed. All 22 desktop/mobile Playwright flows passed, including duplicate history imports, account mismatch rejection, both chart modes, freshness filters, route visit counting, and export pagination with synthetic server responses.
- 13 TypeScript tests passed, covering aggregation deduplication, freshness vs visits, period filters, old backup compatibility, counter merging, invalid imports, and proportional non-overlapping treemap geometry. Existing content checks and 1,355 differential checks also passed.
- Native app built for iPhone 17 Pro Simulator. Eight unit tests and three UI tests passed; the new UI flow opens the progress dashboard and switches treemap/stacked-bar views. Follow-up model changes were rechecked with the unit suite.
- Desktop/mobile dashboard screenshots inspected. No horizontal viewport overflow after fixing the hidden import input.
- Signed-in LeetCode submission response fields were observed in the user's browser. Actual headless export requires the separate browser session's one-time sign-in; anonymous access returned a sign-in/challenge response. Synthetic pagination tests do not establish the completeness of a real account's export.

## Diagnostic familiarity update · 2026-09-27

- Web production build passed. The 22 existing desktop/mobile flows passed; all four new diagnostic flows passed after correcting a scroll effect. The diagnostic checks cover reveal-gated ratings, revising all three flags, reload persistence, exact pattern aggregation, stable sessions, skipping, and reassessment of uncertain ratings.
- All 17 TypeScript tests passed alongside the curriculum and authored algorithm checks. New tests cover sampling across 12 concepts, exact approach attribution, community collection separation, backup merging, invalid records, and keeping diagnostic ratings independent of practice freshness and recall.
- Native iOS built and passed 10 model tests and four UI tests on iPhone 17 Pro Simulator. The diagnostic UI test opens solutions, saves “Probably got it,” and opens the summary. The diagnostic model suite was rechecked after isolating its storage fixtures.
- Visually inspected the diagnostic on desktop/mobile web and native iOS, plus the web familiarity dashboard. Small-phone filter controls use a single column to keep selected labels readable.
- Diagnostic data remains local with portable backup support. No independent-solving ability or mastery is inferred from solution recognition.

## Authenticated history import update · 2026-09-27

- Verified a real authenticated headless export, including partial-history preservation when LeetCode denied further pagination. The account's current completion list was captured separately; private account data remains in `.local/`.
- Verified a subsequent 30-day headless update and cumulative merge without losing older submissions. The command keeps a previous-file backup and does not copy personal data into deployable assets.
- Production web build and all 18 core tests passed. Existing 26 browser flows passed, and the two new desktop/mobile completion-snapshot flows passed after correcting an exact-label test selector. These verify all-time coverage, exclusion from date-filtered coverage, unchanged diagnostic ratings, and persistence.
- All 15 native tests passed (11 model tests, four UI tests). New model checks cover completion snapshots, missing practice dates, file/deep-link imports, preserved drafts, and invalid import URLs.
- Current completion snapshots establish accepted coverage, not when a submission occurred. Full historical submission retrieval remains limited by the records LeetCode makes available; physical-device transfer still uses Files/AirDrop.
