# Submission history and progress dashboard

Both apps have a progress dashboard with category/pattern coverage, a weighted treemap, stacked bars, adjustable hierarchy depth, difficulty and level filters, a submission log, freshness, refocus suggestions, and page-entry counts.

## Headless updates (recommended for repeated use)

From the repository:

```sh
npm ci
npx playwright install chromium
npm run history:login
npm run history:update -- --days 0
# Later, refresh the last 30 days and merge into the same private file:
npm run history:update
# Import automatically and open your dedicated study browser:
npm run history:open
# Optional: also deliver the import to an installed iOS Simulator app:
npm run history:update -- --simulator YOUR_SIMULATOR_UDID
```

The login command opens a separate browser for a one-time LeetCode sign-in. It waits up to ten minutes, verifies the signed-in account, saves its isolated browser session under `.local/leetcode-browser/`, and closes the browser. Subsequent exports run headlessly, without interacting with your Chrome/Comet windows. If LeetCode expires the session or presents a challenge, complete it with `history:login` and retry. The tool stops on authentication/challenge failures; it does not circumvent them.

`history:update` merges new records into **`.local/leetcode-history.json`**, retains the previous file as `.local/leetcode-history.previous.json`, and keeps older submissions during recent or partial exports. An account mismatch stops the merge. Use `--days 0` after a gap longer than 30 days. `--from path.json` merges an existing export without contacting LeetCode. A valid partial export is useful and is clearly identified as partial.

`history:open` opens the deployed web app in a dedicated persistent Chromium profile, imports the cumulative file through the app's normal import control, and verifies it survives a reload. The visible browser stays open until you close it. Close that browser before running the command again. `npm run history:open -- --headless` applies and verifies an import without showing a window. Study drafts and progress remain in git-ignored `.local/atlas-browser/`, separate from the LeetCode sign-in session and from your regular Comet/Chrome profiles. The import stays in browser storage; it is not published to Azure.

`--through YYYY-MM-DD` includes submissions through the end of that day in the computer's local time zone. It defaults to today and rejects future dates. `--out path.json` chooses the output file. By default, private exports and the browser session stay in git-ignored `.local/`, with restrictive filesystem permissions. Do not commit that directory. The session is sensitive even though exported history contains no credentials.

On **web**, open Your progress → Import LeetCode history and select `.local/leetcode-history.json` (in the Mac file picker, press ⇧⌘G to enter the full path). On **iOS**, transfer it with Files/AirDrop and open it in Pattern Atlas, or use Progress → Import LeetCode history. The optional simulator flag stages that same JSON in the selected app's Documents folder and opens its import link; it does not erase app data. Neither app uploads personal history to Azure or automatically watches the output file. Physical iPhones still require transferring/importing the file.

## Browser exporter alternative

[leetcode-export.user.js](../apps/web/public/tools/leetcode-export.user.js) can be copied from the web dashboard and run in the developer console on `https://leetcode.com/progress/` while signed in. It can also be installed in a userscript manager. It adds a small panel with:

- Include submissions through a selected date (default today).
- Export all available history.
- Update the last 30 days.
- Stop and save partial history.

Both exporters paginate `/api/submissions/` with a delay between requests, follow `has_next` and `last_key`, retry rate limits/server errors, detect stalled pagination, and keep partial results after interruption or failure. They use the account's own session on LeetCode. The submission endpoint can include code in its response; only ID, slug, title, timestamp, result, and language are retained in the export. Passwords, cookies, tokens, and code are never written into it.

They also capture the authenticated `/api/problems/all/` completion list as a separate `completions` snapshot (`observedAt` and problem `slugs`) when exporting through today. This fills older accepted-coverage gaps when detailed submissions are unavailable. A snapshot has no submission dates, language, or submission IDs: none are invented. Historical cutoff exports omit the current snapshot because it cannot establish which problems were solved before that date. A cutoff does not delete data already imported by a previous update.

“Reached the oldest available record” means the endpoint reported no next page, not an independent guarantee that LeetCode exposes every historical submission. A partial update preserves older imported records. Use a full export for initial setup and after a long gap. Export timing, date cutoff, deleted records, site retention, catalog scope, and overlapping topic memberships may make app counts differ from LeetCode's summary.

## Meaning of the dashboard

- **Accepted**: at least one imported Accepted result in the selected submission period. All-time coverage also includes the completion snapshot. Date-filtered coverage excludes that undated snapshot. A later failed attempt does not erase prior acceptance.
- **Attempted without acceptance**: submissions exist in that period, but none were accepted.
- **No recorded attempt**: no imported attempt in that period. With a partial history, this is not proof the problem was never attempted on LeetCode.
- **Fresh**: at least one submission (any result) or self-rated recall review within the chosen 7/14/30/60/90-day window. This is recent practice, not measured mastery. Freshness always uses all available practice, independently of the submission-period filter.
- **Needs refresh**: practice exists, but the last practice predates the freshness window.
- **No dated practice**: no timestamped submission or recall review is recorded locally. The problem may still be completed according to the snapshot; its practice date is unknown.
- **Where to refocus**: authored patterns ranked by due review count, then stale practiced problems, then patterns already started, Core priority, and remaining accepted-coverage gaps. Suggestions respect the selected category and problem difficulty.
- **Entries**: opening or returning to a page increments a per-device counter. Editing, revealing a solution, and changing filters do not. Category chart entries include that category and descendant category/pattern pages. The page-entry table reports each actual page separately, including problem pages. Counts start when this release is used; prior navigation cannot be reconstructed.

A problem may belong to several patterns and collections. Tile area represents memberships; category/global counts deduplicate IDs within their scope. Summing adjacent tiles can therefore exceed the parent total. Accepted coverage of a pattern does not prove the submitted solution used that technique. Drill down, filter, or use the accessible list/table for small tiles.

## Diagnostic familiarity

The diagnostic presents solution sets without an editor or a required answer. A set contains the implementations for one problem and one explicitly mapped approach. Open the solutions before choosing a rating:

- **Definitely got it**: I understand the approach and could explain it.
- **Probably got it**: the idea makes sense, but I am unsure of some steps.
- **Did not get it**: I need to study this approach again.
- **Unassessed**: no rating exists; this means unknown, not unfamiliar.

Choose a category or pattern, problem difficulty, and 10, 20, 50, or all eligible sets. The default library covers all 200 authored patterns. An optional community library adds source-collection solution sets. Sampling rotates across root concepts and patterns; within those groups, unseen sets precede prior ratings, followed by uncertainty, oldest assessment, difficulty, and problem number. Each started session keeps its selection stable as ratings change. Skip, go back, revise a rating, or finish early to see the selection summary. Ratings save immediately. Returning with **Unassessed only** continues the remaining material; **Probably / did not get it** targets uncertain ratings.

The familiarity dashboard aggregates the three ratings and unassessed counts by the next hierarchy level or by individual pattern/collection. Filter by category, search by name, or show only groups with uncertain ratings and start a focused diagnostic. The latest assessment date records when the self-report was made. There is no inferred mastery score.

A rating applies only to the approach actually shown. It does not automatically credit every pattern or official tag attached to the problem. Community collections are broad practice groupings; their ratings remain separate from exact authored patterns. Parent concepts aggregate the mapped solution sets beneath them, so a problem with different solution approaches can contribute more than one set.

These self-assessments do not change accepted submissions, drafts, recall scheduling, review activity, or practice freshness. Recognition after seeing a solution is different from recalling an approach independently. Page-entry tracking still records diagnostic navigation normally.

## Portable data

The existing version-1 backup retains `cards`, `drafts`, `bookmarks`, and `activity`, with optional `leetcode`, `visits`, and `familiarity` fields. Old backups still load. New exports can be shared between current web/native releases. Older releases may ignore the new fields.

Imports validate first, preserve existing local drafts, merge reviews by their review date, and reject histories from a different LeetCode account. Visit counters are partitioned by device; repeated imports take the maximum count for each device/page and sum across devices, avoiding duplicate counts. Submission IDs deduplicate repeated/overlapping exports. Unknown catalog slugs remain in the submission log and are counted as unmatched, not assigned to invented patterns.

Familiarity records use `problemId:patternId` keys with a `rating` (`definitely`, `probably`, or `not-yet`) and ISO `assessedAt` timestamp. The newest assessment wins during backup merge. Equal timestamps use the weaker rating so merge order cannot accidentally inflate familiarity. Invalid ratings or timestamps reject the import before local data changes.

All local imports are limited to 10 MB. Browser storage capacity varies; the web app reports persistence failures and offers backup export. Export backups to preserve data before clearing browser storage or removing the app.
