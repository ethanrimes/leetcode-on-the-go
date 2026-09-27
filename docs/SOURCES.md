# Sources and editorial policy

References checked on 2026-09-27:

- [EndlessCheng's algorithm directory](https://github.com/EndlessCheng/codeforces-go): reference for fine-grained technique families, including DP, data structures, strings, and graphs.
- [Requested dynamic-programming outline](https://leetcode.cn/discuss/post/3581838/fen-xiang-gun-ti-dan-dong-tai-gui-hua-ru-007o/): successfully retrieved directly after the browser retrieval timed out. Inspected its full outline and problem groupings, including knapsack, partitions, state machines, interval/subset/digit/tree/game/probability DP, and optimization families.
- [labuladong's algorithm roadmap](https://labuladong.online/en/roadmap/algo/): reference for connecting traversal, subproblems, and data structures.
- [LeetCode problem catalog](https://leetcode.com/problemset/) and public `/api/problems/all/`: factual problem IDs, titles, slugs, and difficulty.
- Each category links to its relevant official LeetCode topic page.

The curriculum is independently written, with original concise problem restatements and Python implementations, not copies of third-party editorials. Examples are authored for learning. Pattern importance is an editorial learning priority, not a measured company/interview frequency.

All 12 EndlessCheng guide pages linked from the GitHub algorithm directory were retrieved directly. Only factual section headings and problem associations are retained in `packages/content/reference-index.json`; guide prose and code are not redistributed. Labuladong's full public directory, fast-track plan, complete-plan overview, and foundational chapter overview informed the coverage audit. Paid articles were not copied or assumed to have been read. The 75 official LeetCode tags were retrieved via the public `questionTopicTags` query. A paginated `questionList` query returned 3,650 tag records, of which 3,629 matched this catalog snapshot; missing tags are explicitly left unknown.

See [COVERAGE.md](COVERAGE.md) for all 200 worked leaves, all 75 official tag dispositions, and the 313-section reference crosswalk. Source sections often span several techniques; extra links under a pattern are labeled as related source-section problems rather than exact leaf assignments.

“Coverage” means the checked-in curriculum, not a claim to enumerate every possible algorithm or every future LeetCode problem. The catalog is a dated reference snapshot; worked study cards are explicitly distinguished from reference-only catalog entries. The catalog covers the public algorithms endpoint, not all SQL, shell, concurrency, or JavaScript-specific tracks. Advanced contest techniques and language-specific tracks can be added under the same unlimited-depth schema.
