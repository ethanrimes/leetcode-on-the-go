# Submission history and progress dashboard

Both apps have a progress dashboard with category/pattern coverage, a weighted treemap, stacked bars, adjustable hierarchy depth, difficulty and level filters, a submission log, freshness, refocus suggestions, and page-entry counts.

## Headless updates (recommended for repeated use)

From the repository:

```sh
npm ci
npx playwright install chromium
npm run history:login
npm run history:export -- --through 2026-09-27
# Later, refresh the last 30 days (use a full export after longer gaps):
npm run history:export -- --days 30
```

The login command opens a separate browser for a one-time LeetCode sign-in. It waits up to ten minutes, verifies the signed-in account, and saves its isolated browser session under `.local/leetcode-browser/`. Subsequent exports run headlessly, without interacting with your Chrome/Comet windows. If LeetCode expires the session or presents a challenge, complete it with `history:login` and retry. The tool stops on authentication/challenge failures; it does not circumvent them.

`--through YYYY-MM-DD` includes submissions through the end of that day in the computer's local time zone. It defaults to today and rejects future dates. `--out path.json` chooses the output file. By default, private exports and the browser session stay in git-ignored `.local/`, with restrictive filesystem permissions. Do not commit that directory. The session is sensitive even though exported history contains no credentials.

On **web**, open Your progress → Import LeetCode history and select the generated JSON. On **iOS**, transfer it with Files/AirDrop and use Progress → Import LeetCode history. Refreshing fetches new records; importing merges them by submission ID. Neither app uploads personal history to Azure or automatically watches the output file.

## Browser exporter alternative

[leetcode-export.user.js](../apps/web/public/tools/leetcode-export.user.js) can be copied from the web dashboard and run in the developer console on `https://leetcode.com/progress/` while signed in. It can also be installed in a userscript manager. It adds a small panel with:

- Include submissions through a selected date (default today).
- Export all available history.
- Update the last 30 days.
- Stop and save partial history.

Both exporters paginate `/api/submissions/` with a delay between requests, follow `has_next` and `last_key`, retry rate limits/server errors, detect stalled pagination, and keep partial results after interruption or failure. They use the account's own session on LeetCode. The submission endpoint can include code in its response; only ID, slug, title, timestamp, result, and language are retained in the export. Passwords, cookies, tokens, and code are never written into it.

“Reached the oldest available record” means the endpoint reported no next page, not an independent guarantee that LeetCode exposes every historical submission. A partial update preserves older imported records. Use a full export for initial setup and after a long gap. Export timing, date cutoff, deleted records, site retention, catalog scope, and overlapping topic memberships may make app counts differ from LeetCode's summary.

## Meaning of the dashboard

- **Accepted**: at least one imported Accepted result for the problem in the selected submission period. A later failed attempt does not erase that acceptance.
- **Attempted without acceptance**: submissions exist in that period, but none were accepted.
- **No recorded attempt**: no imported attempt in that period. With a partial history, this is not proof the problem was never attempted on LeetCode.
- **Fresh**: at least one submission (any result) or self-rated recall review within the chosen 7/14/30/60/90-day window. This is recent practice, not measured mastery. Freshness always uses all available practice, independently of the submission-period filter.
- **Needs refresh**: practice exists, but the last practice predates the freshness window.
- **Never practiced**: no submission or recall review is recorded locally.
- **Where to refocus**: authored patterns ranked by due review count, then stale practiced problems, then patterns already started, Core priority, and remaining accepted-coverage gaps. Suggestions respect the selected category and problem difficulty.
- **Entries**: opening or returning to a page increments a per-device counter. Editing, revealing a solution, and changing filters do not. Category chart entries include that category and descendant category/pattern pages. The page-entry table reports each actual page separately, including problem pages. Counts start when this release is used; prior navigation cannot be reconstructed.

A problem may belong to several patterns and collections. Tile area represents memberships; category/global counts deduplicate IDs within their scope. Summing adjacent tiles can therefore exceed the parent total. Accepted coverage of a pattern does not prove the submitted solution used that technique. Drill down, filter, or use the accessible list/table for small tiles.

## Portable data

The existing version-1 backup retains `cards`, `drafts`, `bookmarks`, and `activity`, with optional `leetcode` and `visits` fields. Old backups still load. New exports can be shared between current web/native releases. Older releases may ignore the new fields.

Imports validate first, preserve existing local drafts, merge reviews by their review date, and reject histories from a different LeetCode account. Visit counters are partitioned by device; repeated imports take the maximum count for each device/page and sum across devices, avoiding duplicate counts. Submission IDs deduplicate repeated/overlapping exports. Unknown catalog slugs remain in the submission log and are counted as unmatched, not assigned to invented patterns.

All local imports are limited to 10 MB. Browser storage capacity varies; the web app reports persistence failures and offers backup export. Export backups to preserve data before clearing browser storage or removing the app.
