# Pattern Atlas — LeetCode on the go

A study-first monorepo for recognizing algorithmic patterns, recalling their invariants, drafting solutions, and reviewing canonical implementations.

**Live web app:** https://blue-sea-0c03ac51e.3.azurestaticapps.net

The current curriculum contains **200 worked patterns**, **2,909 problems with revealable Python solutions**, **12 topic roots**, and a **4,068-problem reference catalog**. It was audited against the 12 EndlessCheng guide outlines, labuladong’s public algorithm directory and learning plans, and all 75 official LeetCode topic tags. Read the [coverage audit](docs/COVERAGE.md) for the complete hierarchy and the explicitly listed specialist extensions; this is broad algorithm coverage, not a claim of literal exhaustiveness.

The solution library includes **193 authored lessons** and **2,716 additional community cards**, with MIT attribution to walkccc. The hierarchy now includes **313 source-guide practice collections** plus official-topic collections. Community cards link to the official statement and examples on LeetCode; they preserve upstream Python code and public signatures.

The Graphite design uses charcoal, slate, and blue, compact topic indexes, and sortable problem tables. Every leaf supports difficulty, number, and title ordering, with a saved preference per collection.

Features include recursive topic navigation, pattern and problem difficulty labels, original summaries, recognition cues, pitfalls, a Python editor with automatic local draft saving, multiple solution approaches where included, solution reveal, self-rated spaced review, solution-recognition diagnostics, bookmarks, a progress dashboard with treemaps and stacked bars, practice freshness, refocus suggestions, submission history, page-entry tracking, and portable JSON backups. The iOS app is native SwiftUI and includes the worked curriculum offline.

- `apps/web`: React + TypeScript, responsive browser study workspace.
- `apps/ios`: native SwiftUI iPhone/iPad app, with an offline curriculum.
- `api`: private Azure Functions history API backed by Azure Table Storage.
- `packages/content`: versioned curriculum shared by both apps.
- `packages/core`: typed curriculum queries and review scheduling.
- `scripts`: content authoring, validation, and resource generation.
- `infrastructure`: Azure hosting and repeatable deployment.

## Development

Requires Node 22.12+, Python 3.10+, and npm. iOS additionally requires Xcode 16+ and XcodeGen.

```sh
npm install
npm run build
npm run dev
npm test
npm run test:e2e
npm run ios:generate
open apps/ios/PatternAtlas.xcodeproj
```

Select the `PatternAtlas` scheme and an iPhone simulator. To install on a physical device, select your Apple development team in Xcode’s Signing & Capabilities settings. No developer signing credentials are checked into this repo.

For Azure deployment, run `npm run deploy` after authenticating the Azure CLI to the configured subscription. The dedicated resource group is `leetcode-on-the-go-rg`; the web app and managed API use Azure Static Web Apps Free, with a private Azure Storage table for LeetCode history. GitHub Actions validates web/content changes before deploying `main`. The deployment token is held in a GitHub secret. See [architecture](docs/ARCHITECTURE.md), [source methodology](docs/SOURCES.md), and [verification evidence](docs/VALIDATION.md).

LeetCode completions and submissions sync through the private Azure API after owner authentication. Drafts, ratings, and page visits stay on the current device; export/import remains available for backups. Running code and submitting solutions happen on LeetCode.

## Diagnose concept and pattern familiarity

Open **Diagnostic test** on web or **Progress → Start diagnostic test** on iOS. No answer is required: open a solution set, follow the reasoning, and choose **Definitely got it**, **Probably got it**, or **Did not get it**. Choose a category, difficulty, and session length; work through unassessed material or revisit uncertain ratings.

Ratings save immediately and appear in **Your progress → Concept & pattern familiarity** on web and **Progress → Familiarity by concept & pattern** on iOS. The report shows the three ratings and unassessed sets at concept or individual-pattern level. Diagnostics cover all 200 authored patterns by default, with an option to include community solution collections. They measure self-reported familiarity independently of submissions, recall scheduling, and practice freshness. See [the progress guide](docs/PROGRESS.md#diagnostic-familiarity) for attribution and backup behavior.

## Curriculum approach

Organize knowledge as topic → technique family → subfamily → individual pattern. Each node has an approach and teaching guidance; each leaf connects to worked problem cards. Difficulty of a problem is separate from the learning level and priority of its pattern. Problems may demonstrate more than one pattern.

Core lesson summaries, explanations, and code are authored for this project. Additional community code is imported from a pinned MIT-licensed walkccc commit; see [the expanded library report](docs/PROBLEM_LIBRARY.md). LeetCode titles, IDs, difficulty, and URLs are reference metadata. No paid editorials or hidden test cases are included. See `docs/SOURCES.md` for reference methodology and coverage boundaries.

This project is independent of LeetCode, EndlessCheng, and labuladong.

Third-party licenses and dependency attribution are in [THIRD_PARTY.md](docs/THIRD_PARTY.md).

## Import your LeetCode history

Run `npm run history:login` once to sign in in an isolated browser, then `npm run history:update -- --days 0` for the initial import. Repeat `npm run history:update` for headless 30-day updates. After Azure provisioning, each update uploads the cumulative file to the private table and verifies it through the API. `npm run history:sync` retries an upload without scraping. In the hosted web app, sign in with the owner GitHub account or enter the private sync key. On iOS, enter the sync key in Progress → Azure history. The key is generated in git-ignored `.local/cloud-sync-key` during deployment; never commit or share it publicly. `--simulator UDID` delivers the history and key to an installed native simulator app. Both apps merge repeated imports without duplicates. `--through YYYY-MM-DD` sets a submission cutoff.

The exporter captures both available dated submissions and a current completed-problem snapshot. This lets accepted coverage include older completions even when LeetCode limits detailed history. Missing dates remain unknown and do not inflate freshness or diagnostic ratings. Personal exports and sessions are never bundled into the public app.

A browser-console/userscript exporter is also available in the web dashboard. See [the progress guide](docs/PROGRESS.md) for setup, freshness definitions, and data coverage limitations. Private exports and the isolated browser session are excluded from Git.
