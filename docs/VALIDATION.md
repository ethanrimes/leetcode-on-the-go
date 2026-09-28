# Verification evidence

Verified on 2026-09-27. These results describe observed checks, not a guarantee that every algorithm passes LeetCode's private judge.

| Check | Observed result |
| --- | --- |
| Production web build | Passed TypeScript and Vite production compilation |
| Curriculum integrity | 836 nodes: 12 roots, 221 authored patterns, 313 source practice collections, 2,911 problems with solutions; references, hierarchy, and bundled web/iOS parity passed |
| Community integrity | 2,697 additional cards passed Python syntax, source SHA-256, attribution, and membership checks; imported code was not executed |
| Authored solution examples | All 221 pattern examples passed |
| Seeded algorithm checks | 1,355 differential/property checks passed, covering prefix counting, subarray/window methods, monotonic structures, string algorithms, range queries, lazy propagation, SCCs, and LFU eviction |
| Shared study logic | 25 tests passed, including source calendar reconciliation, UTC dates, selected-year streaks, and snapshot merge compatibility |
| Local browser flows | All 40 Playwright tests passed across desktop and mobile viewports |
| Deployed browser flows | Current release smoke checked on Azure: progress, activity, and four multi-select filters loaded; 34 earlier production browser flows passed |
| Native iOS | All 18 tests passed on iPhone 17 Pro Simulator, including 14 model tests and four UI study flows |
| Azure content | HTTPS returned 200; hosted curriculum matched the repository content byte for byte |
| Azure private history | Uploaded the authenticated export and read back all 637 completion snapshot slugs and 400 dated submissions from Table Storage |
| Hosted account | GitHub sign-in in Comet loaded 637 completed problems and 400 dated submissions from Azure; a fresh headless browser retained the same data after reload |
| Cloud API | Unauthenticated history GET returned 401; five history-store tests passed, including calendar persistence across old-client uploads |

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
- Native physical-device signing, TestFlight, and App Store submission have not been performed. [TestFlight preparation](TESTFLIGHT.md) records the release configuration and current account/tooling blockers.
- LeetCode completion and submission history now synchronizes through the private Azure history API. Drafts, diagnostic ratings, recall reviews, and page visits remain device-local and can be moved with explicit JSON export/import.
- The reference catalog is larger than the set of worked cards. The [coverage audit](COVERAGE.md) lists rare specialist extensions and non-algorithm topics outside the current worked curriculum.
- GitHub Actions runs web validation before deployment. Individual workflow results are available in the repository's Actions tab.

## LeetCode activity reconciliation · 2026-09-27

- The old REST importer had retained only 400 submission details, including 299 in 2025. The chart used that incomplete list as its yearly activity total and calculated streaks across all years. LeetCode's live `userCalendar(year: 2025)` instead reported 1,272 submissions, 49 active days, and a 13-day streak.
- The GraphQL `submissionList` exporter reached the oldest available record and recovered 1,883 details. Every UTC day matched the independently fetched source calendars: 494 submissions / 24 active days / 12-day longest streak in 2024; 1,272 / 49 / 13 in 2025; 117 / 5 / 3 in 2026. There were zero daily count mismatches across all three years. The 2025 records contained 835 accepted results. These are private account observations at the export time; exports remain git-ignored.
- Web and native now preserve source calendar snapshots alongside details, use UTC day boundaries, scope longest streak to the selected year, and show current streak only for the current year. Missing individual results are explicitly distinguished from source-reported zero activity. Older-client uploads retain calendar snapshots in Azure.
- A headless browser imported the recovered file and verified the 2025 figures, the matching-total note, and the rendered chart. The production web build and all 40 browser flows passed. The native build and all 18 simulator checks passed. All 25 core tests, five API tests, curriculum checks, and 1,355 algorithm checks passed.

## Curriculum and progress exploration update · 2026-09-27

- Rebuilt the shared web/iOS curriculum from the three coverage audits: 221 authored patterns, 2,911 solution cards, and 836 hierarchy nodes. All 172 distinct official topic slugs in the checked-in catalog now route to practice collections. The 433 catalog references without topic or source-guide metadata remain unassigned to a specific pattern; the audits list further specialist authored-lesson gaps.
- Curriculum parity, all 221 authored examples, all 2,697 community card integrity checks, 1,355 seeded differential checks, 22 shared logic tests, and four API tests passed. The community implementations were not executed against LeetCode's judge.
- The web progress screen now places coverage before familiarity, supports multi-select filters, draws nested category frames, opens a tile's problem list in a new tab, and shows a clickable dated activity calendar. A dense 707-tile view was visually inspected, including its 129 group frames.
- The production web build and all 38 desktop/mobile browser flows passed after a hover-card click-through correction. Browser checks include multi-filter unions, frame rendering, hover/focus details, new-tab tile navigation, and day-specific submission lists.
- The native progress screen adds the same filter combinations, grouped coverage, problem navigation, and an activity calendar with day details. All 16 simulator tests passed after adjusting the diagnostic flow for the longer progress screen.
- GitHub Actions validated and deployed commit `5330702`. The hosted curriculum matched the committed JSON byte for byte, a fresh headless browser loaded the progress/activity UI and four multi-select filters, and the private Azure history API read back 637 completion slugs and 400 dated submissions after sync.

## Azure history sync · 2026-09-27

- Deployed the managed API and private Azure Table Storage in the project's resource group. The API accepts only the authorized GitHub identity or the private sync key.
- Uploaded the cumulative private export, then fetched it from Azure and verified every local submission ID and completion slug was present. An unauthenticated request was rejected.
- Signed into the deployed site in Comet and observed 637 completed problems and 400 dated submissions in the progress dashboard. A separate fresh headless browser loaded the same figures before and after reload.
- Production web build, 34 desktop/mobile browser flows, 21 shared core tests, 3 history-store tests, and 16 native simulator tests passed. The native app was rebuilt after the final staged-key import adjustment.

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
- Imported the actual private history into the native Simulator and verified its completion/submission totals. The dedicated persistent study browser imported the same file on the deployed site, merged repeated imports without duplicates, and retained its summary after a reload. `history:open --headless` completed successfully. The existing Comet window did not respond to keyboard actions during the import attempt; its storage is separate from the verified study-browser profile.
- Current completion snapshots establish accepted coverage, not when a submission occurred. Full historical submission retrieval remains limited by the records LeetCode makes available; physical-device transfer still uses Files/AirDrop.

## Progress exploration and recommendations · 2026-09-27

- Replaced web system select popups with shared styled menus. Verified desktop/mobile bounds, keyboard navigation, Escape/focus restoration, catalog sorting persistence, and diagnostic filters.
- Added viewport-constrained treemap hover/focus details, preserving click/tap study links. Visual inspection caught and corrected clipped popup content and pointer-focus interference with taps.
- Added matching web/iOS recommendations from exact worked-solution mappings, with explicit reasons, direct problem links, duplicate suppression, and topic diversity. Unknown completion dates remain unknown. Tests cover newer successful attempts, review precedence, filters, uncertainty, and future submission exclusion.
- Web production build, all 21 core tests, and all 34 desktop/mobile browser flows passed. The browser suite ran against the production preview after the existing development server reported an outdated dependency cache.
- Native build succeeded. Fifteen native tests passed initially; the remaining progress UI test passed after updating its navigation for the imported-history summary and longer recommendation section. All 16 native checks have passing results.
- Inspected the private account's six recommendations against its imported records and viewed the resulting web layout. Personal exports, screenshots, and sessions remain git-ignored.
