# Sources and editorial policy

References checked on 2026-09-27:

- [EndlessCheng's algorithm directory](https://github.com/EndlessCheng/codeforces-go): reference for fine-grained technique families, including DP, data structures, strings, and graphs.
- [Requested dynamic-programming outline](https://leetcode.cn/discuss/post/3581838/fen-xiang-gun-ti-dan-dong-tai-gui-hua-ru-007o/): successfully retrieved directly after the browser retrieval timed out. Inspected its full outline and problem groupings, including knapsack, partitions, state machines, interval/subset/digit/tree/game/probability DP, and optimization families.
- [labuladong's algorithm roadmap](https://labuladong.online/en/roadmap/algo/): reference for connecting traversal, subproblems, and data structures.
- [LeetCode problem catalog](https://leetcode.com/problemset/) and public `/api/problems/all/`: factual problem IDs, titles, slugs, and difficulty.
- Each category links to its relevant official LeetCode topic page.

The 214 core lessons are independently written, with original concise problem restatements and Python implementations. An additional 2,697 community cards preserve MIT-licensed Python implementations from [walkccc/LeetCode](https://github.com/walkccc/LeetCode), pinned at commit `9b85aa15e086d0b5dc1ead7184bca547942e6ff6`. These cards provide an official statement link instead of a copied problem statement. Examples are authored for learning. Pattern importance is an editorial learning priority, not a measured company/interview frequency.

All 12 EndlessCheng guide pages linked from the GitHub algorithm directory were retrieved directly. Only factual section headings and problem associations are retained in `packages/content/reference-index.json`; guide prose and code are not redistributed. Labuladong's full public directory, fast-track plan, complete-plan overview, and foundational chapter overview informed the coverage audit. Paid articles were not copied or assumed to have been read. The 75 official LeetCode tags were retrieved via the public `questionTopicTags` query. A paginated `questionList` query returned 3,650 tag records, of which 3,629 matched this catalog snapshot; missing tags are explicitly left unknown.

See [COVERAGE.md](COVERAGE.md) for the original 200 worked leaves and the linked 21 new leaves, all 75 official tag dispositions, and the 313-section reference crosswalk. Source sections often span several techniques; extra links under a pattern are labeled as related source-section problems rather than exact leaf assignments.

“Coverage” means the checked-in curriculum, not a claim to enumerate every possible algorithm or every future LeetCode problem. The catalog is a dated reference snapshot; worked study cards are explicitly distinguished from reference-only catalog entries. The catalog covers the public algorithms endpoint, not all SQL, shell, concurrency, or JavaScript-specific tracks. Advanced contest techniques and language-specific tracks can be added under the same unlimited-depth schema.

## Community import and classification

`scripts/import_community.py` imports Python code from a local checkout, preserves source bytes, records SHA-256 hashes and commit-specific links, and copies the complete MIT notice into the repository, hosted web assets, and native app resources. The committed `community-solutions.json` makes ordinary builds independent of network access. It contains 2,897 upstream problem IDs and 3,165 valid Python files; four upstream files with syntax errors were excluded and recorded. Existing authored lessons take precedence over imported variants for their problem IDs.

Only authored implementations execute in curriculum tests. Imported implementations receive syntax, source-hash, metadata, and attribution checks; they are not claimed to pass LeetCode's private judge. Some implementations depend on LeetCode's provided imports and node classes.

All 313 source sections have stable collection IDs and English navigation labels in `scripts/content/practice_paths.py`. Problem membership follows the pinned source index. Broader official-topic collections preserve factual tag membership. These associations do not assert that a particular imported implementation follows the source guide's technique; the UI makes this distinction explicit. Original pattern pages also offer related practice from surrounding source sections.
