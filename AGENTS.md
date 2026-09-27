# Repository conventions

- Work from this monorepo; keep web and native iOS features consistent where their platform affordances allow.
- Community code must retain MIT attribution, pinned source links, and unmodified-code hashes. Do not execute community imports during validation; syntax-check them. Preserve the distinction between authored pattern lessons, source practice collections, and official-topic groups.
- Author curriculum changes in `scripts/content/`, then run `npm run content:build`. Generated JSON is checked in so both apps are usable without authoring dependencies.
- Preserve stable node/problem IDs and the version-1 portable backup shape. Never replace a user's existing drafts during import.
- Do not copy third-party guide prose, paid editorials, or hidden test cases. Use original explanations and code with explicit source links for factual references.
- Never label a reference-only catalog problem as a worked card. Keep coverage claims aligned with `docs/COVERAGE.md`.
- Run `npm test` after changing content or scheduling. Run `npm run test:e2e` for changed web study flows. Regenerate with XcodeGen and build/test iOS for SwiftUI or model changes.
- Keep user code execution on LeetCode. Internal curriculum validation may execute only checked-in authored solutions.
- Azure resources are isolated in `leetcode-on-the-go-rg`. Do not alter unrelated resources. Keep deployment credentials out of files and command output.
