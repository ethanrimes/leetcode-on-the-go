# Curriculum coverage audit

Reviewed 2026-09-27. This document distinguishes worked lessons from source references; a broad tag match is not evidence that every technique within that tag is covered.

## Published curriculum

- 836 hierarchy nodes, including 12 topic roots, 221 authored patterns, and 313 source-guide practice collections.
- 2,911 unique problems with local solutions: 214 authored lessons and 2,697 additional community cards. See [PROBLEM_LIBRARY.md](PROBLEM_LIBRARY.md) for collection membership and source provenance.
- 221 independently authored Python implementations, each checked against its example.
- 4,068 factual problem references from LeetCode’s algorithms catalog snapshot.
- 3,629 catalog entries matched current official topic metadata; unmatched entries remain searchable without invented tags.
- 12 EndlessCheng guides retrieved directly and inspected, yielding 313 problem-bearing sections.
- Labuladong: reviewed the full public algorithm directory, roadmap, quick learning plan, complete-plan overview, and data-structure chapter overview. Paid articles were not copied or treated as read.

The pattern table below records the original 200 worked leaves. The 21 added leaves and their problem anchors are documented in the [DP/graph](COVERAGE_DP_GRAPHS.md) and [foundation](COVERAGE_FOUNDATIONS.md) audits. The [mapping audit](COVERAGE_MAPPING.md) accounts for all 172 tagged topic slugs in the catalog and identifies 433 entries that still lack both tag and guide association.

## Audit decisions

The required core is recognition patterns used across standard algorithm problems, plus the advanced families surfaced by the reference guides: all principal knapsack variants, sequence/interval/tree/digit/subset/probability DP, optimized transitions, graph components and shortest paths, monotone structures, mutable range structures, string automata, suffix arrays, and geometry. Pattern importance is an editorial learning priority rather than an interview-frequency statistic.

Examples of important distinctions preserved: fixed versus variable windows; longest versus shortest windows; exactly-k versus at-most-k counting; zero-one versus reusable versus bounded versus grouped knapsack; ordered versus unordered counting; node-state versus visited-subset graph search; ordinary versus weighted union-find; plain versus lazy versus sparse segment trees; and different solutions for the same problem.

### Remaining specialist extensions

The three references are living resources, not a finite universal definition of every algorithmic pattern. This edition does **not** claim literal exhaustiveness. Further contest-focused lessons remain for persistent/rollback structures, Mo’s algorithm, splay trees, heavy-light and centroid decomposition, virtual trees, tree knapsack, convex-hull-trick and WQS DP, general max-flow/min-cost-flow, suffix automata, XOR linear bases, Möbius inversion, FFT/NTT/FWT, and generating functions. Related source sections are now browsable practice collections, and many include attributed community implementations. They remain distinct from fully authored pattern lessons.

SQL/database, shell, concurrency, and language-specific API exercises are separate tracks outside this algorithm-focused edition. These boundaries are visible in both apps.

## Official LeetCode tags

The following original authored-lesson audit accounts for every official tag. Community additions do not silently change these authored-coverage claims. “Represented” identifies worked examples carrying the official tag; manual mappings identify aliases or techniques intentionally used by our own implementation.

| Official tag | Coverage | Worked anchor IDs or technique |
|---|---|---|
| Array | Represented | 1, 49, 128, 560, 974, 238, 1109, 1314, 41, 169, 54, 167 … |
| Hash Table | Represented | 1, 49, 128, 560, 974, 41, 169, 3, 76, 992, 424, 139 … |
| Linked List | Represented | 206, 19, 141, 21, 146, 460, 622, 25, 234 |
| Math | Represented | 70, 233, 486, 227, 1071, 204, 50, 172, 96, 149, 398, 528 … |
| Two Pointers | Represented | 167, 15, 11, 283, 75, 19, 141, 295, 1755, 28, 5, 2406 … |
| String | Represented | 49, 3, 76, 424, 91, 474, 1143, 72, 115, 139, 516, 127 … |
| Binary Search | Represented | 167, 35, 33, 162, 4, 875, 410, 1552, 300, 354, 1235, 1631 … |
| Divide and Conquer | Represented | 169, 4, 53, 215, 307, 315, 912, 347, 191, 105 |
| Dynamic Programming | Represented | 410, 70, 198, 213, 53, 152, 2466, 91, 416, 494, 474, 322 … |
| Backtracking | Represented | 494, 526, 78, 46, 40, 39, 22, 79, 52, 698, 131, 37 |
| Stack | Represented | 20, 1047, 394, 227, 739, 84, 907, 316, 155, 232, 341, 234 … |
| Heap | Technique / legacy alias mapped | Bounded top-k heap |
| Greedy | Represented | 11, 410, 714, 316, 435, 2406, 55, 45, 134, 630, 763, 1024 |
| Bit Manipulation | Represented | 526, 78, 1755, 187, 421, 136, 191, 201, 898, 698, 847, 982 … |
| Tree | Represented | 104, 102, 437, 236, 98, 230, 543, 124, 337, 834, 968, 96 … |
| Depth-First Search | Represented | 200, 417, 785, 207, 329, 2360, 743, 787, 1631, 684, 332, 1192 … |
| Breadth-First Search | Represented | 322, 200, 994, 417, 785, 127, 207, 329, 2360, 743, 2290, 787 … |
| Union-Find | Represented | 128, 200, 785, 1631, 684, 1584, 399, 1697 |
| Graph Theory | Represented | 785, 207, 329, 2360, 743, 2290, 787, 1334, 684, 1584, 332, 1192 … |
| Design | Represented | 295, 307, 146, 155, 232, 208, 732, 384, 380, 460, 341, 622 … |
| Topological Sort | Represented | 207, 329, 2360, 802 |
| Trie | Represented | 139, 208, 421, 792 |
| Binary Indexed Tree | Represented | 673, 307, 315 |
| Segment Tree | Represented | 673, 307, 315, 2569, 732 |
| Binary Search Tree | Represented | 98, 230, 96 |
| Recursion | Represented | 233, 486, 206, 21, 394, 10, 50, 509, 25, 234 |
| Brainteaser | Represented | 292 |
| Memoization | Represented | 70, 139, 329, 698, 509 |
| Queue | Represented | 1696, 239, 232, 862, 341, 622 |
| Minimax | Represented | 486, 292 |
| Reservoir Sampling | Represented | 398 |
| Ordered Map | Technique / legacy alias mapped | LRU order plus key lookup |
| Geometry | Represented | 149, 587 |
| Rejection Sampling | Represented | 470 |
| Sliding Window | Represented | 643, 3, 76, 992, 424, 239, 187, 862, 713, 1044 |
| Sweep Line | Represented | 986 |
| Rolling Hash | Represented | 2223, 187, 1044 |
| Suffix Array | Represented | 2223, 1044 |
| Meet in the Middle | Represented | 1755 |
| Database | Separate non-algorithm track | See scope above |
| Shell | Separate non-algorithm track | See scope above |
| Concurrency | Separate non-algorithm track | See scope above |
| Sorting | Represented | 49, 169, 15, 75, 1552, 354, 1235, 332, 215, 295, 1755, 792 … |
| Heap (Priority Queue) | Represented | 1696, 743, 2290, 787, 1631, 332, 239, 215, 373, 295, 2406, 630 … |
| Merge Sort | Represented | 315, 912 |
| String Matching | Represented | 28, 2223 |
| Matrix | Represented | 1314, 54, 64, 221, 200, 994, 417, 329, 2290, 1631, 79, 1463 … |
| Monotonic Stack | Represented | 739, 84, 907, 316, 42 |
| Simulation | Represented | 54 |
| Combinatorics | Represented | 1201, 62 |
| Binary Tree | Represented | 104, 102, 437, 236, 98, 230, 543, 124, 337, 968, 96, 105 … |
| Doubly-Linked List | Represented | 146, 460 |
| Interactive | Represented | 374 |
| Bucket Sort | Represented | 912, 347, 164 |
| Radix Sort | Represented | 912, 164 |
| Counting | Represented | 169, 992, 347 |
| Data Stream | Represented | 295 |
| Iterator | Represented | 341 |
| Hash Function | Represented | 2223, 187, 1044 |
| Enumeration | Represented | 204 |
| Number Theory | Represented | 204, 1201 |
| Prefix Sum | Represented | 560, 974, 238, 1109, 1314, 410, 2406, 528, 2218, 862, 713, 732 |
| Quickselect | Represented | 215, 347 |
| Ordered Set | Represented | 315, 732 |
| Monotonic Queue | Represented | 1696, 239, 862 |
| Counting Sort | Represented | 912 |
| Game Theory | Represented | 486, 292 |
| Eulerian Circuit | Represented | 332 |
| Randomized | Represented | 398, 528, 470, 384, 380 |
| Shortest Path | Represented | 743, 2290, 787, 1334, 399 |
| Bitmask | Represented | 526, 1755, 698, 847 |
| Probability and Statistics | Represented | 470 |
| Minimum Spanning Tree | Represented | 1584 |
| Biconnected Component | Represented | 1192 |
| Strongly Connected Component | Technique / legacy alias mapped | Strongly connected component condensation |

## Worked pattern inventory

Every leaf below has recognition cues, an approach, a pitfall, a learning level, priority, a problem summary, and a revealable Python implementation.

| Hierarchical path | Level | Priority | Worked LeetCode problems |
|---|---|---|---|
| Arrays & hashing / Lookup & counting / Complement lookup | Foundation | Core | [1. Two Sum](https://leetcode.com/problems/two-sum/) |
| Arrays & hashing / Lookup & counting / Frequency signatures | Foundation | Core | [49. Group Anagrams](https://leetcode.com/problems/group-anagrams/) |
| Arrays & hashing / Lookup & counting / Sequence boundary detection | Intermediate | Core | [128. Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) |
| Arrays & hashing / Prefix & difference / Prefix sum with frequency map | Intermediate | Core | [560. Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) |
| Arrays & hashing / Prefix & difference / Remainder classes | Intermediate | Useful | [974. Subarray Sums Divisible by K](https://leetcode.com/problems/subarray-sums-divisible-by-k/) |
| Arrays & hashing / Prefix & difference / Prefix and suffix products | Intermediate | Core | [238. Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) |
| Arrays & hashing / Prefix & difference / Range updates with differences | Intermediate | Useful | [1109. Corporate Flight Bookings](https://leetcode.com/problems/corporate-flight-bookings/) |
| Arrays & hashing / Prefix & difference / Two-dimensional prefix sums | Intermediate | Useful | [1314. Matrix Block Sum](https://leetcode.com/problems/matrix-block-sum/) |
| Arrays & hashing / In-place structure / Index placement | Advanced | Useful | [41. First Missing Positive](https://leetcode.com/problems/first-missing-positive/) |
| Arrays & hashing / In-place structure / Boyer–Moore cancellation | Foundation | Useful | [169. Majority Element](https://leetcode.com/problems/majority-element/) |
| Arrays & hashing / In-place structure / Matrix boundary simulation | Foundation | Useful | [54. Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) |
| Two pointers & windows / Opposing & forward pointers / Opposing pointers on sorted values | Foundation | Core | [167. Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) |
| Two pointers & windows / Opposing & forward pointers / Fix one, solve two-sum | Intermediate | Core | [15. 3Sum](https://leetcode.com/problems/3sum/) |
| Two pointers & windows / Opposing & forward pointers / Move the limiting boundary | Intermediate | Core | [11. Container With Most Water](https://leetcode.com/problems/container-with-most-water/) |
| Two pointers & windows / Opposing & forward pointers / Read/write compaction | Foundation | Core | [283. Move Zeroes](https://leetcode.com/problems/move-zeroes/) |
| Two pointers & windows / Opposing & forward pointers / Three-way partition | Intermediate | Useful | [75. Sort Colors](https://leetcode.com/problems/sort-colors/) |
| Two pointers & windows / Sliding windows / Fixed-length rolling window | Foundation | Core | [643. Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/) |
| Two pointers & windows / Sliding windows / Longest valid window | Intermediate | Core | [3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) |
| Two pointers & windows / Sliding windows / Shortest covering window | Advanced | Core | [76. Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) |
| Two pointers & windows / Sliding windows / Exactly k via at most k | Advanced | Useful | [992. Subarrays with K Different Integers](https://leetcode.com/problems/subarrays-with-k-different-integers/) |
| Two pointers & windows / Sliding windows / Replacement-budget window | Intermediate | Useful | [424. Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) |
| Binary search / Ordered positions / Lower bound | Foundation | Core | [35. Search Insert Position](https://leetcode.com/problems/search-insert-position/) |
| Binary search / Ordered positions / Rotated sorted search | Intermediate | Core | [33. Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) |
| Binary search / Ordered positions / Peak by slope | Intermediate | Useful | [162. Find Peak Element](https://leetcode.com/problems/find-peak-element/) |
| Binary search / Ordered positions / Partition two sorted arrays | Advanced | Specialist | [4. Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) |
| Binary search / Search on the answer / Minimum feasible rate | Intermediate | Core | [875. Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) |
| Binary search / Search on the answer / Minimize the maximum partition | Advanced | Core | [410. Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) |
| Binary search / Search on the answer / Maximize the minimum separation | Intermediate | Useful | [1552. Magnetic Force Between Two Balls](https://leetcode.com/problems/magnetic-force-between-two-balls/) |
| Dynamic programming / Linear sequences / Fibonacci-style counting | Foundation | Core | [70. Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) |
| Dynamic programming / Linear sequences / Take or skip adjacent items | Foundation | Core | [198. House Robber](https://leetcode.com/problems/house-robber/) |
| Dynamic programming / Linear sequences / Break a cycle into paths | Intermediate | Useful | [213. House Robber II](https://leetcode.com/problems/house-robber-ii/) |
| Dynamic programming / Linear sequences / Kadane: extend or restart | Foundation | Core | [53. Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) |
| Dynamic programming / Linear sequences / Track both extrema | Intermediate | Useful | [152. Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) |
| Dynamic programming / Linear sequences / Count by reachable length | Intermediate | Core | [2466. Count Ways To Build Good Strings](https://leetcode.com/problems/count-ways-to-build-good-strings/) |
| Dynamic programming / Linear sequences / Decode with local transitions | Intermediate | Useful | [91. Decode Ways](https://leetcode.com/problems/decode-ways/) |
| Dynamic programming / Knapsack / Zero-one choices / Subset-sum feasibility | Intermediate | Core | [416. Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) |
| Dynamic programming / Knapsack / Zero-one choices / Signed choices to subset counts | Intermediate | Useful | [494. Target Sum](https://leetcode.com/problems/target-sum/) |
| Dynamic programming / Knapsack / Zero-one choices / Multiple resource budgets | Intermediate | Useful | [474. Ones and Zeroes](https://leetcode.com/problems/ones-and-zeroes/) |
| Dynamic programming / Knapsack / Reusable choices / Unbounded minimum cost | Intermediate | Core | [322. Coin Change](https://leetcode.com/problems/coin-change/) |
| Dynamic programming / Knapsack / Reusable choices / Unordered combination counts | Intermediate | Core | [518. Coin Change II](https://leetcode.com/problems/coin-change-ii/) |
| Dynamic programming / Knapsack / Reusable choices / Ordered composition counts | Intermediate | Useful | [377. Combination Sum IV](https://leetcode.com/problems/combination-sum-iv/) |
| Dynamic programming / Grids & multiple sequences / Grid path accumulation | Foundation | Core | [64. Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) |
| Dynamic programming / Grids & multiple sequences / Longest common subsequence | Intermediate | Core | [1143. Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) |
| Dynamic programming / Grids & multiple sequences / Edit distance | Intermediate | Core | [72. Edit Distance](https://leetcode.com/problems/edit-distance/) |
| Dynamic programming / Grids & multiple sequences / Count matching subsequences | Advanced | Useful | [115. Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/) |
| Dynamic programming / Grids & multiple sequences / Maximal square ending at a cell | Intermediate | Useful | [221. Maximal Square](https://leetcode.com/problems/maximal-square/) |
| Dynamic programming / Subsequences / LIS with minimal tails | Intermediate | Core | [300. Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) |
| Dynamic programming / Subsequences / Sort one dimension, reverse ties | Advanced | Useful | [354. Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) |
| Dynamic programming / Subsequences / Count optimal subsequences | Intermediate | Useful | [673. Number of Longest Increasing Subsequence](https://leetcode.com/problems/number-of-longest-increasing-subsequence/) |
| Dynamic programming / State machines / Hold and cash states | Intermediate | Core | [714. Best Time to Buy and Sell Stock with Transaction Fee](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/) |
| Dynamic programming / State machines / Cooldown state | Intermediate | Useful | [309. Best Time to Buy and Sell Stock with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) |
| Dynamic programming / Partitions & intervals / Prefix segmentation | Intermediate | Core | [139. Word Break](https://leetcode.com/problems/word-break/) |
| Dynamic programming / Partitions & intervals / Palindrome interval recurrence | Intermediate | Core | [516. Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/) |
| Dynamic programming / Partitions & intervals / Choose the last operation | Advanced | Core | [312. Burst Balloons](https://leetcode.com/problems/burst-balloons/) |
| Dynamic programming / Partitions & intervals / Weighted interval scheduling | Advanced | Useful | [1235. Maximum Profit in Job Scheduling](https://leetcode.com/problems/maximum-profit-in-job-scheduling/) |
| Dynamic programming / Compressed & advanced states / Subset bitmask assignment | Advanced | Useful | [526. Beautiful Arrangement](https://leetcode.com/problems/beautiful-arrangement/) |
| Dynamic programming / Compressed & advanced states / Digit DP with tight bound | Advanced | Specialist | [233. Number of Digit One](https://leetcode.com/problems/number-of-digit-one/) |
| Dynamic programming / Compressed & advanced states / Game DP as score difference | Intermediate | Useful | [486. Predict the Winner](https://leetcode.com/problems/predict-the-winner/) |
| Dynamic programming / Compressed & advanced states / Probability propagation | Advanced | Useful | [688. Knight Probability in Chessboard](https://leetcode.com/problems/knight-probability-in-chessboard/) |
| Dynamic programming / Compressed & advanced states / Monotone deque optimized DP | Advanced | Useful | [1696. Jump Game VI](https://leetcode.com/problems/jump-game-vi/) |
| Dynamic programming / Compressed & advanced states / Profile tiling states | Advanced | Specialist | [790. Domino and Tromino Tiling](https://leetcode.com/problems/domino-and-tromino-tiling/) |
| Graphs & grids / Traversal & components / Flood-fill connected components | Foundation | Core | [200. Number of Islands](https://leetcode.com/problems/number-of-islands/) |
| Graphs & grids / Traversal & components / Multi-source BFS | Intermediate | Core | [994. Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) |
| Graphs & grids / Traversal & components / Reverse reachability | Intermediate | Useful | [417. Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) |
| Graphs & grids / Traversal & components / Bipartite coloring | Intermediate | Core | [785. Is Graph Bipartite?](https://leetcode.com/problems/is-graph-bipartite/) |
| Graphs & grids / Traversal & components / Bidirectional BFS | Advanced | Useful | [127. Word Ladder](https://leetcode.com/problems/word-ladder/) |
| Graphs & grids / Directed order / Kahn topological sorting | Intermediate | Core | [207. Course Schedule](https://leetcode.com/problems/course-schedule/) |
| Graphs & grids / Directed order / Memoized DFS on a DAG | Advanced | Core | [329. Longest Increasing Path in a Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) |
| Graphs & grids / Directed order / Functional-graph cycle peeling | Advanced | Useful | [2360. Longest Cycle in a Graph](https://leetcode.com/problems/longest-cycle-in-a-graph/) |
| Graphs & grids / Shortest paths / Dijkstra with stale-entry skipping | Intermediate | Core | [743. Network Delay Time](https://leetcode.com/problems/network-delay-time/) |
| Graphs & grids / Shortest paths / Zero-one BFS | Advanced | Useful | [2290. Minimum Obstacle Removal to Reach Corner](https://leetcode.com/problems/minimum-obstacle-removal-to-reach-corner/) |
| Graphs & grids / Shortest paths / Bounded-edge Bellman–Ford | Intermediate | Useful | [787. Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) |
| Graphs & grids / Shortest paths / Floyd–Warshall all-pairs closure | Intermediate | Useful | [1334. Find the City With the Smallest Number of Neighbors at a Threshold Distance](https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/) |
| Graphs & grids / Shortest paths / Minimax path relaxation | Intermediate | Useful | [1631. Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/) |
| Graphs & grids / Connectivity & structure / Union-find cycle detection | Intermediate | Core | [684. Redundant Connection](https://leetcode.com/problems/redundant-connection/) |
| Graphs & grids / Connectivity & structure / Minimum spanning tree: Prim | Intermediate | Core | [1584. Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) |
| Graphs & grids / Connectivity & structure / Eulerian path: Hierholzer | Advanced | Useful | [332. Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary/) |
| Graphs & grids / Connectivity & structure / Bridges with low-link values | Advanced | Specialist | [1192. Critical Connections in a Network](https://leetcode.com/problems/critical-connections-in-a-network/) |
| Trees & linked lists / Binary tree traversal / Postorder subtree aggregation | Foundation | Core | [104. Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) |
| Trees & linked lists / Binary tree traversal / Breadth-first levels | Foundation | Core | [102. Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) |
| Trees & linked lists / Binary tree traversal / Ancestor state with prefix counts | Intermediate | Useful | [437. Path Sum III](https://leetcode.com/problems/path-sum-iii/) |
| Trees & linked lists / Binary tree traversal / Lowest common ancestor | Intermediate | Core | [236. Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) |
| Trees & linked lists / Binary tree traversal / BST bounds invariant | Intermediate | Core | [98. Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) |
| Trees & linked lists / Binary tree traversal / Iterative inorder selection | Intermediate | Core | [230. Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) |
| Trees & linked lists / Tree dynamic programming / Diameter from two best branches | Foundation | Core | [543. Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) |
| Trees & linked lists / Tree dynamic programming / Maximum path gain | Advanced | Core | [124. Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) |
| Trees & linked lists / Tree dynamic programming / Tree independent set | Intermediate | Core | [337. House Robber III](https://leetcode.com/problems/house-robber-iii/) |
| Trees & linked lists / Tree dynamic programming / Rerooting with subtree sizes | Advanced | Useful | [834. Sum of Distances in Tree](https://leetcode.com/problems/sum-of-distances-in-tree/) |
| Trees & linked lists / Tree dynamic programming / Greedy camera states | Advanced | Useful | [968. Binary Tree Cameras](https://leetcode.com/problems/binary-tree-cameras/) |
| Trees & linked lists / Linked list pointers / Iterative pointer reversal | Foundation | Core | [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) |
| Trees & linked lists / Linked list pointers / Fixed-gap deletion | Intermediate | Core | [19. Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) |
| Trees & linked lists / Linked list pointers / Floyd cycle meeting | Foundation | Core | [141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) |
| Trees & linked lists / Linked list pointers / Merge sorted chains | Foundation | Core | [21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) |
| Stacks, heaps & range queries / Stack discipline / Matching delimiters | Foundation | Core | [20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) |
| Stacks, heaps & range queries / Stack discipline / Adjacent cancellation | Foundation | Useful | [1047. Remove All Adjacent Duplicates In String](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/) |
| Stacks, heaps & range queries / Stack discipline / Nested decoding contexts | Intermediate | Core | [394. Decode String](https://leetcode.com/problems/decode-string/) |
| Stacks, heaps & range queries / Stack discipline / Arithmetic precedence stack | Intermediate | Useful | [227. Basic Calculator II](https://leetcode.com/problems/basic-calculator-ii/) |
| Stacks, heaps & range queries / Monotone structures / Next greater element | Intermediate | Core | [739. Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) |
| Stacks, heaps & range queries / Monotone structures / Histogram span boundaries | Advanced | Core | [84. Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) |
| Stacks, heaps & range queries / Monotone structures / Contribution counting with tie ownership | Advanced | Useful | [907. Sum of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums/) |
| Stacks, heaps & range queries / Monotone structures / Monotone deque window extrema | Advanced | Core | [239. Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) |
| Stacks, heaps & range queries / Monotone structures / Lexicographic monotone subsequence | Intermediate | Useful | [316. Remove Duplicate Letters](https://leetcode.com/problems/remove-duplicate-letters/) |
| Stacks, heaps & range queries / Priority queues / Bounded top-k heap | Intermediate | Core | [215. Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) |
| Stacks, heaps & range queries / Priority queues / Merge k sorted streams | Intermediate | Useful | [373. Find K Pairs with Smallest Sums](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/) |
| Stacks, heaps & range queries / Priority queues / Two heaps around the median | Advanced | Core | [295. Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) |
| Stacks, heaps & range queries / Mutable range queries / Fenwick tree point updates | Advanced | Core | [307. Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) |
| Stacks, heaps & range queries / Mutable range queries / Iterative segment tree | Advanced | Useful | [307. Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) |
| Stacks, heaps & range queries / Mutable range queries / Coordinate compression and inversion counts | Advanced | Useful | [315. Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) |
| Stacks, heaps & range queries / Data structure design / LRU order plus key lookup | Intermediate | Core | [146. LRU Cache](https://leetcode.com/problems/lru-cache/) |
| Stacks, heaps & range queries / Data structure design / Min stack with aggregate snapshots | Foundation | Core | [155. Min Stack](https://leetcode.com/problems/min-stack/) |
| Stacks, heaps & range queries / Data structure design / Amortized queue using two stacks | Foundation | Useful | [232. Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/) |
| Backtracking & enumeration / Choice trees / Subsets: include or exclude | Foundation | Core | [78. Subsets](https://leetcode.com/problems/subsets/) |
| Backtracking & enumeration / Choice trees / Permutations with a used set | Foundation | Core | [46. Permutations](https://leetcode.com/problems/permutations/) |
| Backtracking & enumeration / Choice trees / Duplicate-aware combinations | Intermediate | Core | [40. Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) |
| Backtracking & enumeration / Choice trees / Reusable combinations | Intermediate | Core | [39. Combination Sum](https://leetcode.com/problems/combination-sum/) |
| Backtracking & enumeration / Choice trees / Prefix-valid generation | Intermediate | Core | [22. Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) |
| Backtracking & enumeration / Constraint search / Grid path backtracking | Intermediate | Core | [79. Word Search](https://leetcode.com/problems/word-search/) |
| Backtracking & enumeration / Constraint search / Column and diagonal occupancy | Advanced | Useful | [52. N-Queens II](https://leetcode.com/problems/n-queens-ii/) |
| Backtracking & enumeration / Constraint search / Meet in the middle | Advanced | Useful | [1755. Closest Subsequence Sum](https://leetcode.com/problems/closest-subsequence-sum/) |
| Strings & tries / Matching & palindrome structure / KMP failure links | Intermediate | Core | [28. Find the Index of the First Occurrence in a String](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/) |
| Strings & tries / Matching & palindrome structure / Z-function prefix matches | Advanced | Useful | [2223. Sum of Scores of Built Strings](https://leetcode.com/problems/sum-of-scores-of-built-strings/) |
| Strings & tries / Matching & palindrome structure / Expand around centers | Intermediate | Core | [5. Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) |
| Strings & tries / Matching & palindrome structure / Manacher palindrome radii | Advanced | Specialist | [5. Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) |
| Strings & tries / Matching & palindrome structure / Rolling hash with collision verification | Intermediate | Useful | [187. Repeated DNA Sequences](https://leetcode.com/problems/repeated-dna-sequences/) |
| Strings & tries / Matching & palindrome structure / Regex state DP | Advanced | Useful | [10. Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) |
| Strings & tries / Prefix indexes / Trie exact and prefix lookup | Intermediate | Core | [208. Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) |
| Strings & tries / Prefix indexes / Bitwise trie for maximum XOR | Advanced | Useful | [421. Maximum XOR of Two Numbers in an Array](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/) |
| Strings & tries / Prefix indexes / Subsequence position index | Intermediate | Useful | [792. Number of Matching Subsequences](https://leetcode.com/problems/number-of-matching-subsequences/) |
| Greedy & intervals / Interval decisions / Merge overlapping intervals | Intermediate | Core | [56. Merge Intervals](https://leetcode.com/problems/merge-intervals/) |
| Greedy & intervals / Interval decisions / Earliest-finish scheduling | Intermediate | Core | [435. Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) |
| Greedy & intervals / Interval decisions / Sweep-line overlap count | Intermediate | Useful | [2406. Divide Intervals Into Minimum Number of Groups](https://leetcode.com/problems/divide-intervals-into-minimum-number-of-groups/) |
| Greedy & intervals / Reachability & exchange / Farthest reachable frontier | Intermediate | Core | [55. Jump Game](https://leetcode.com/problems/jump-game/) |
| Greedy & intervals / Reachability & exchange / Jump layers as implicit BFS | Intermediate | Core | [45. Jump Game II](https://leetcode.com/problems/jump-game-ii/) |
| Greedy & intervals / Reachability & exchange / Reset after negative balance | Intermediate | Useful | [134. Gas Station](https://leetcode.com/problems/gas-station/) |
| Greedy & intervals / Reachability & exchange / Regret heap scheduling | Advanced | Useful | [630. Course Schedule III](https://leetcode.com/problems/course-schedule-iii/) |
| Greedy & intervals / Reachability & exchange / Partition by last occurrence | Intermediate | Useful | [763. Partition Labels](https://leetcode.com/problems/partition-labels/) |
| Sorting & selection / Merge-sort divide and conquer | Foundation | Core | [912. Sort an Array](https://leetcode.com/problems/sort-an-array/) |
| Sorting & selection / Randomized quickselect | Intermediate | Useful | [215. Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) |
| Sorting & selection / Frequency buckets | Intermediate | Core | [347. Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) |
| Sorting & selection / Radix sorting fixed-width digits | Advanced | Specialist | [164. Maximum Gap](https://leetcode.com/problems/maximum-gap/) |
| Bits, math & geometry / Bit representations / XOR cancellation | Foundation | Core | [136. Single Number](https://leetcode.com/problems/single-number/) |
| Bits, math & geometry / Bit representations / Remove the lowest set bit | Foundation | Core | [191. Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) |
| Bits, math & geometry / Bit representations / Common binary prefix | Intermediate | Useful | [201. Bitwise AND of Numbers Range](https://leetcode.com/problems/bitwise-and-of-numbers-range/) |
| Bits, math & geometry / Bit representations / Distinct suffix-OR compression | Advanced | Useful | [898. Bitwise ORs of Subarrays](https://leetcode.com/problems/bitwise-ors-of-subarrays/) |
| Bits, math & geometry / Number theory & counting / Euclidean gcd structure | Foundation | Useful | [1071. Greatest Common Divisor of Strings](https://leetcode.com/problems/greatest-common-divisor-of-strings/) |
| Bits, math & geometry / Number theory & counting / Sieve of Eratosthenes | Intermediate | Core | [204. Count Primes](https://leetcode.com/problems/count-primes/) |
| Bits, math & geometry / Number theory & counting / Exponentiation by squaring | Intermediate | Core | [50. Pow(x, n)](https://leetcode.com/problems/powx-n/) |
| Bits, math & geometry / Number theory & counting / Prime valuation in factorials | Foundation | Useful | [172. Factorial Trailing Zeroes](https://leetcode.com/problems/factorial-trailing-zeroes/) |
| Bits, math & geometry / Number theory & counting / Catalan decomposition | Intermediate | Useful | [96. Unique Binary Search Trees](https://leetcode.com/problems/unique-binary-search-trees/) |
| Bits, math & geometry / Geometry & randomness / Normalized slope counting | Advanced | Useful | [149. Max Points on a Line](https://leetcode.com/problems/max-points-on-a-line/) |
| Bits, math & geometry / Geometry & randomness / Reservoir sampling | Intermediate | Useful | [398. Random Pick Index](https://leetcode.com/problems/random-pick-index/) |
| Bits, math & geometry / Geometry & randomness / Weighted prefix sampling | Intermediate | Useful | [528. Random Pick with Weight](https://leetcode.com/problems/random-pick-with-weight/) |
| Dynamic programming / Knapsack / Grouped prefix choices | Advanced | Useful | [2218. Maximum Value of K Coins From Piles](https://leetcode.com/problems/maximum-value-of-k-coins-from-piles/) |
| Dynamic programming / Knapsack / Bounded multiplicity counting | Advanced | Useful | [2585. Number of Ways to Earn Points](https://leetcode.com/problems/number-of-ways-to-earn-points/) |
| Dynamic programming / Compressed & advanced states / Subset partition with remainder | Advanced | Useful | [698. Partition to K Equal Sum Subsets](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/) |
| Dynamic programming / Compressed & advanced states / Visited-set shortest walk | Advanced | Useful | [847. Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) |
| Dynamic programming / Compressed & advanced states / SOS subset aggregation | Advanced | Specialist | [982. Triples with Bitwise AND Equal To Zero](https://leetcode.com/problems/triples-with-bitwise-and-equal-to-zero/) |
| Dynamic programming / Grids & multiple sequences / Two simultaneous walkers | Advanced | Useful | [1463. Cherry Pickup II](https://leetcode.com/problems/cherry-pickup-ii/) |
| Dynamic programming / Partitions & intervals / Minimum-cut palindrome partition | Advanced | Useful | [132. Palindrome Partitioning II](https://leetcode.com/problems/palindrome-partitioning-ii/) |
| Dynamic programming / Compressed & advanced states / Digit DP with uniqueness mask | Advanced | Specialist | [2376. Count Special Integers](https://leetcode.com/problems/count-special-integers/) |
| Dynamic programming / Compressed & advanced states / Prefix-sum transition optimization | Advanced | Specialist | [629. K Inverse Pairs Array](https://leetcode.com/problems/k-inverse-pairs-array/) |
| Dynamic programming / Compressed & advanced states / Matrix exponentiation of transitions | Advanced | Specialist | [509. Fibonacci Number](https://leetcode.com/problems/fibonacci-number/) |
| Two pointers & windows / Sliding windows / Shortest signed-sum window with deque | Advanced | Useful | [862. Shortest Subarray with Sum at Least K](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/) |
| Two pointers & windows / Sliding windows / Count valid window suffixes | Intermediate | Core | [713. Subarray Product Less Than K](https://leetcode.com/problems/subarray-product-less-than-k/) |
| Two pointers & windows / Opposing & forward pointers / Two sorted interval streams | Intermediate | Useful | [986. Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/) |
| Arrays & hashing / In-place structure / Grouped run scanning | Foundation | Useful | [1446. Consecutive Characters](https://leetcode.com/problems/consecutive-characters/) |
| Binary search / Search on the answer / Kth value via cumulative counts | Advanced | Useful | [378. Kth Smallest Element in a Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) |
| Graphs & grids / Connectivity & structure / Weighted union-find potentials | Advanced | Useful | [399. Evaluate Division](https://leetcode.com/problems/evaluate-division/) |
| Graphs & grids / Connectivity & structure / Kruskal edge selection | Intermediate | Useful | [1584. Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) |
| Graphs & grids / Connectivity & structure / Strongly connected component condensation | Advanced | Specialist | [802. Find Eventual Safe States](https://leetcode.com/problems/find-eventual-safe-states/) |
| Graphs & grids / Connectivity & structure / Bipartite matching by augmenting paths | Advanced | Specialist | [1820. Maximum Number of Accepted Invitations](https://leetcode.com/problems/maximum-number-of-accepted-invitations/) |
| Stacks, heaps & range queries / Mutable range queries / Lazy segment tree range flips | Advanced | Specialist | [2569. Handling Sum Queries After Update](https://leetcode.com/problems/handling-sum-queries-after-update/) |
| Stacks, heaps & range queries / Mutable range queries / Dynamic sparse segment tree | Advanced | Specialist | [732. My Calendar III](https://leetcode.com/problems/my-calendar-iii/) |
| Stacks, heaps & range queries / Mutable range queries / Sparse table idempotent queries | Advanced | Specialist | [239. Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) |
| Stacks, heaps & range queries / Mutable range queries / Square-root decomposition | Intermediate | Useful | [307. Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) |
| Graphs & grids / Connectivity & structure / Offline sorted-threshold connectivity | Advanced | Useful | [1697. Checking Existence of Edge Length Limited Paths](https://leetcode.com/problems/checking-existence-of-edge-length-limited-paths/) |
| Strings & tries / Matching & palindrome structure / Suffix array and adjacent LCP | Advanced | Specialist | [1044. Longest Duplicate Substring](https://leetcode.com/problems/longest-duplicate-substring/) |
| Strings & tries / Prefix indexes / Aho–Corasick multi-pattern matching | Advanced | Specialist | [139. Word Break](https://leetcode.com/problems/word-break/) |
| Strings & tries / Matching & palindrome structure / Minimal cyclic rotation | Advanced | Specialist | [899. Orderly Queue](https://leetcode.com/problems/orderly-queue/) |
| Bits, math & geometry / Geometry & randomness / Convex hull with cross products | Advanced | Specialist | [587. Erect the Fence](https://leetcode.com/problems/erect-the-fence/) |
| Bits, math & geometry / Number theory & counting / Inclusion–exclusion with LCM | Advanced | Useful | [1201. Ugly Number III](https://leetcode.com/problems/ugly-number-iii/) |
| Bits, math & geometry / Geometry & randomness / Rejection sampling without modulo bias | Intermediate | Useful | [470. Implement Rand10() Using Rand7()](https://leetcode.com/problems/implement-rand10-using-rand7/) |
| Bits, math & geometry / Geometry & randomness / Fisher–Yates shuffle | Intermediate | Useful | [384. Shuffle an Array](https://leetcode.com/problems/shuffle-an-array/) |
| Stacks, heaps & range queries / Data structure design / Random access with swap-delete | Intermediate | Core | [380. Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/) |
| Stacks, heaps & range queries / Data structure design / LFU frequency buckets | Advanced | Useful | [460. LFU Cache](https://leetcode.com/problems/lfu-cache/) |
| Stacks, heaps & range queries / Data structure design / Lazy nested iterator | Intermediate | Useful | [341. Flatten Nested List Iterator](https://leetcode.com/problems/flatten-nested-list-iterator/) |
| Stacks, heaps & range queries / Data structure design / Circular buffer queue | Foundation | Useful | [622. Design Circular Queue](https://leetcode.com/problems/design-circular-queue/) |
| Trees & linked lists / Tree dynamic programming / Binary lifting ancestor queries | Advanced | Useful | [1483. Kth Ancestor of a Tree Node](https://leetcode.com/problems/kth-ancestor-of-a-tree-node/) |
| Bits, math & geometry / Number theory & counting / Losing-state modular invariant | Foundation | Useful | [292. Nim Game](https://leetcode.com/problems/nim-game/) |
| Bits, math & geometry / Number theory & counting / Multiplicative combinatorial counting | Foundation | Core | [62. Unique Paths](https://leetcode.com/problems/unique-paths/) |
| Binary search / Ordered positions / Interactive monotone oracle | Foundation | Useful | [374. Guess Number Higher or Lower](https://leetcode.com/problems/guess-number-higher-or-lower/) |
| Trees & linked lists / Binary tree traversal / Reconstruct from traversal boundaries | Intermediate | Core | [105. Construct Binary Tree from Preorder and Inorder Traversal](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) |
| Trees & linked lists / Binary tree traversal / Serialization with null markers | Advanced | Core | [297. Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) |
| Trees & linked lists / Linked list pointers / Reverse a fixed-size group | Advanced | Useful | [25. Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) |
| Trees & linked lists / Linked list pointers / Midpoint split and half reversal | Foundation | Useful | [234. Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/) |
| Backtracking & enumeration / Choice trees / Partition by valid segments | Intermediate | Core | [131. Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) |
| Backtracking & enumeration / Constraint search / Minimum-remaining-values Sudoku search | Advanced | Useful | [37. Sudoku Solver](https://leetcode.com/problems/sudoku-solver/) |
| Two pointers & windows / Opposing & forward pointers / Resolve water from the lower boundary | Advanced | Core | [42. Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) |
| Dynamic programming / Grids & multiple sequences / Reconstruct an optimal sequence | Advanced | Useful | [1092. Shortest Common Supersequence ](https://leetcode.com/problems/shortest-common-supersequence/) |
| Greedy & intervals / Interval decisions / Greedy interval covering | Intermediate | Useful | [1024. Video Stitching](https://leetcode.com/problems/video-stitching/) |

## Source-section crosswalk

The following is a factual index of reference headings and their problem links, not copied guide prose. A worked anchor means we have a local card for at least one problem in that section; it does not assert that the entire section is covered. Each source guide has been inspected to select and separate the important techniques above.

| Guide | Source section | Reference problems | Local worked anchors |
|---|---|---|---|
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 一、定长滑动窗口 / §1.1 基础 | 13 | 643 |
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 一、定长滑动窗口 / §1.2 进阶（选做） | 23 | Reference only |
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 二、不定长滑动窗口 / §2.1 越短越合法/求最长/最大 / §2.1.1 基础 | 11 | 3 |
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 二、不定长滑动窗口 / §2.1 越短越合法/求最长/最大 / §2.1.2 进阶（选做） | 22 | Reference only |
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 二、不定长滑动窗口 / §2.2 越长越合法/求最短/最小 | 7 | 76 |
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 二、不定长滑动窗口 / §2.3 求子数组个数 / §2.3.1 越短越合法 | 7 | 713 |
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 二、不定长滑动窗口 / §2.3 求子数组个数 / §2.3.2 越长越合法 | 8 | Reference only |
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 二、不定长滑动窗口 / §2.3 求子数组个数 / §2.3.3 恰好型滑动窗口 | 5 | 992 |
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 二、不定长滑动窗口 / §2.4 其他（选做） | 8 | 424 |
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 三、单序列双指针 / §3.1 反转字符串 | 14 | Reference only |
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 三、单序列双指针 / §3.2 相向双指针 | 32 | 167, 15, 11, 42 |
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 三、单序列双指针 / §3.3 同向双指针 | 12 | Reference only |
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 三、单序列双指针 / §3.4 背向双指针 | 2 | Reference only |
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 三、单序列双指针 / §3.5 原地修改 | 20 | 283, 75, 41 |
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 三、单序列双指针 / §3.6 矩阵上的双指针 | 2 | Reference only |
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 四、双序列双指针 / §4.1 双指针 | 22 | 986 |
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 四、双序列双指针 / §4.2 判断子序列 | 13 | Reference only |
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 五、三指针 | 7 | Reference only |
| [0viNMK](https://leetcode.cn/circle/discuss/0viNMK/) | 六、分组循环 | 53 | 1446 |
| [SqopEo](https://leetcode.cn/circle/discuss/SqopEo/) | 一、二分查找 / §1.1 基础 | 5 | 35 |
| [SqopEo](https://leetcode.cn/circle/discuss/SqopEo/) | 一、二分查找 / §1.2 进阶 | 22 | Reference only |
| [SqopEo](https://leetcode.cn/circle/discuss/SqopEo/) | 二、二分答案 / §2.1 求最小 / 答疑 | 18 | 875 |
| [SqopEo](https://leetcode.cn/circle/discuss/SqopEo/) | 二、二分答案 / §2.2 求最大 | 17 | Reference only |
| [SqopEo](https://leetcode.cn/circle/discuss/SqopEo/) | 二、二分答案 / §2.3 二分间接值 | 2 | Reference only |
| [SqopEo](https://leetcode.cn/circle/discuss/SqopEo/) | 二、二分答案 / §2.4 最小化最大值 | 15 | 410, 1631 |
| [SqopEo](https://leetcode.cn/circle/discuss/SqopEo/) | 二、二分答案 / §2.5 最大化最小值 | 12 | 1552 |
| [SqopEo](https://leetcode.cn/circle/discuss/SqopEo/) | 二、二分答案 / §2.6 第 K 小/大 | 18 | 378, 1201, 373 |
| [SqopEo](https://leetcode.cn/circle/discuss/SqopEo/) | 三、三分法 | 1 | Reference only |
| [SqopEo](https://leetcode.cn/circle/discuss/SqopEo/) | 四、其他 | 25 | 374, 162, 33, 4 |
| [9oZFK9](https://leetcode.cn/circle/discuss/9oZFK9/) | 一、单调栈 / §1.1 基础 | 5 | 739 |
| [9oZFK9](https://leetcode.cn/circle/discuss/9oZFK9/) | 一、单调栈 / §1.2 进阶 | 31 | Reference only |
| [9oZFK9](https://leetcode.cn/circle/discuss/9oZFK9/) | 二、矩形 | 10 | 84, 221, 42 |
| [9oZFK9](https://leetcode.cn/circle/discuss/9oZFK9/) | 三、贡献法 | 10 | 907 |
| [9oZFK9](https://leetcode.cn/circle/discuss/9oZFK9/) | 四、最小字典序 | 7 | 316 |
| [YiXPXW](https://leetcode.cn/circle/discuss/YiXPXW/) | 一、网格图 DFS | 23 | 200, 417 |
| [YiXPXW](https://leetcode.cn/circle/discuss/YiXPXW/) | 二、网格图 BFS | 23 | 994 |
| [YiXPXW](https://leetcode.cn/circle/discuss/YiXPXW/) | 三、网格图 0-1 BFS | 5 | 2290 |
| [YiXPXW](https://leetcode.cn/circle/discuss/YiXPXW/) | 五、综合应用 | 16 | 1631 |
| [dHn9Vk](https://leetcode.cn/circle/discuss/dHn9Vk/) | 一、基础题 | 26 | 191 |
| [dHn9Vk](https://leetcode.cn/circle/discuss/dHn9Vk/) | 二、异或（XOR）的性质 | 18 | Reference only |
| [dHn9Vk](https://leetcode.cn/circle/discuss/dHn9Vk/) | 三、与或（AND/OR）的性质 | 10 | Reference only |
| [dHn9Vk](https://leetcode.cn/circle/discuss/dHn9Vk/) | 三、与或（AND/OR）的性质 / AND/OR LogTrick | 8 | 898 |
| [dHn9Vk](https://leetcode.cn/circle/discuss/dHn9Vk/) | 三、与或（AND/OR）的性质 / GCD LogTrick | 5 | Reference only |
| [dHn9Vk](https://leetcode.cn/circle/discuss/dHn9Vk/) | 四、拆位 / 贡献法 | 8 | Reference only |
| [dHn9Vk](https://leetcode.cn/circle/discuss/dHn9Vk/) | 五、试填法 | 10 | 421 |
| [dHn9Vk](https://leetcode.cn/circle/discuss/dHn9Vk/) | 六、恒等式 | 2 | Reference only |
| [dHn9Vk](https://leetcode.cn/circle/discuss/dHn9Vk/) | 七、线性基 | 2 | Reference only |
| [dHn9Vk](https://leetcode.cn/circle/discuss/dHn9Vk/) | 八、思维题 | 14 | Reference only |
| [dHn9Vk](https://leetcode.cn/circle/discuss/dHn9Vk/) | 九、其他 | 25 | 136, 201, 982 |
| [01LUak](https://leetcode.cn/circle/discuss/01LUak/) | 一、图的遍历 / §1.1 深度优先搜索（DFS） | 24 | 207, 802 |
| [01LUak](https://leetcode.cn/circle/discuss/01LUak/) | 一、图的遍历 / §1.2 广度优先搜索（BFS） | 8 | Reference only |
| [01LUak](https://leetcode.cn/circle/discuss/01LUak/) | 一、图的遍历 / §1.3 图论建模 + BFS 最短路 | 21 | 322, 847, 127 |
| [01LUak](https://leetcode.cn/circle/discuss/01LUak/) | 二、拓扑排序 / §2.1 拓扑排序 | 15 | 802 |
| [01LUak](https://leetcode.cn/circle/discuss/01LUak/) | 二、拓扑排序 / §2.2 在拓扑序上 DP | 5 | Reference only |
| [01LUak](https://leetcode.cn/circle/discuss/01LUak/) | 二、拓扑排序 / §2.3 基环树 | 9 | 2360, 684 |
| [01LUak](https://leetcode.cn/circle/discuss/01LUak/) | 三、最短路 / §3.1 单源最短路：Dijkstra 算法 | 37 | 743, 1631, 787 |
| [01LUak](https://leetcode.cn/circle/discuss/01LUak/) | 三、最短路 / §3.2 全源最短路：Floyd 算法 | 7 | 1334 |
| [01LUak](https://leetcode.cn/circle/discuss/01LUak/) | 四、最小生成树 | 6 | 1584 |
| [01LUak](https://leetcode.cn/circle/discuss/01LUak/) | 五、欧拉路径/欧拉回路 | 3 | 332 |
| [01LUak](https://leetcode.cn/circle/discuss/01LUak/) | 六、强连通分量/双连通分量 | 3 | 1192 |
| [01LUak](https://leetcode.cn/circle/discuss/01LUak/) | 七、二分图染色 | 3 | 785 |
| [01LUak](https://leetcode.cn/circle/discuss/01LUak/) | 八、网络流 | 16 | 1820 |
| [01LUak](https://leetcode.cn/circle/discuss/01LUak/) | 九、其他 | 17 | 1697 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 一、入门 DP / §1.1 爬楼梯 | 7 | 70, 377, 2466 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 一、入门 DP / §1.2 打家劫舍 / 答疑 | 7 | 198, 213 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 一、入门 DP / §1.3 最大子数组和（最大子段和） | 13 | 53, 152 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 二、网格图 DP | 1 | 64 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 二、网格图 DP / §2.1 基础 | 14 | 64, 62 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 二、网格图 DP / §2.2 进阶 | 14 | 329, 1463 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 三、背包 / §3.1 0-1 背包 | 23 | 416, 494, 474 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 三、背包 / §3.2 完全背包 | 7 | 322, 518 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 三、背包 / §3.3 多重背包（选做） | 4 | 2585 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 三、背包 / §3.4 分组背包 | 3 | 2218 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 三、背包 / §3.5 树上背包（选做） | 2 | Reference only |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 四、经典线性 DP / §4.1 最长公共子序列（LCS） / §4.1.1 基础 | 6 | 1143, 72 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 四、经典线性 DP / §4.1 最长公共子序列（LCS） / §4.1.2 进阶 | 12 | 115, 1092, 10 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 四、经典线性 DP / §4.2 最长递增子序列（LIS） | 1 | Reference only |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 四、经典线性 DP / §4.2 最长递增子序列（LIS） / §4.2.1 基础 | 5 | 300 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 四、经典线性 DP / §4.2 最长递增子序列（LIS） / §4.2.2 进阶 | 15 | 354, 673 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 五、划分型 DP / §5.1 判定能否划分 | 2 | 139 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 五、划分型 DP / §5.2 最优划分 | 21 | 132, 91 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 五、划分型 DP / §5.3 约束划分个数 | 17 | 410 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 六、状态机 DP / §6.1 买卖股票 | 7 | 309, 714 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 六、状态机 DP / §6.2 基础 | 10 | 198 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 六、状态机 DP / §6.3 进阶 | 30 | Reference only |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 七、其他线性 DP / §7.1 一维 DP | 22 | Reference only |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 七、其他线性 DP / §7.2 不相交区间 | 6 | 1235 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 七、其他线性 DP / §7.3 子数组 DP | 11 | 53, 152 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 七、其他线性 DP / §7.4 合法子序列 DP | 20 | Reference only |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 七、其他线性 DP / §7.5 子矩形 DP | 6 | 221 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 七、其他线性 DP / §7.6 多维 DP | 59 | Reference only |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 七、其他线性 DP / §7.7 计数 DP | 5 | Reference only |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 八、区间 DP / §8.1 最长回文子序列 | 8 | 516 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 八、区间 DP / §8.2 区间 DP | 19 | 5, 96, 312 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 九、状态压缩 DP（状压 DP） / §9.1 排列型状压 DP ① 相邻无关 | 12 | 526 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 九、状态压缩 DP（状压 DP） / §9.2 排列型状压 DP ② 相邻相关 | 6 | Reference only |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 九、状态压缩 DP（状压 DP） / §9.3 旅行商问题（TSP） | 5 | 847 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 九、状态压缩 DP（状压 DP） / §9.4 子集状压 DP | 16 | Reference only |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 九、状态压缩 DP（状压 DP） / §9.5 轮廓线 DP | 7 | Reference only |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 九、状态压缩 DP（状压 DP） / §9.6 SOS DP | 5 | Reference only |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 九、状态压缩 DP（状压 DP） / §9.7 其他状压 DP | 10 | 698 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十、数位 DP / §10.1 统计合法元素的数目 | 27 | 2376 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十、数位 DP / §10.2 统计合法元素的价值总和 | 6 | 233 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十、数位 DP / §10.3 其他数位 DP | 2 | Reference only |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十一、优化 DP / §11.1 前缀和优化 DP | 17 | 629 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十一、优化 DP / §11.2 单调栈优化 DP | 4 | Reference only |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十一、优化 DP / §11.3 单调队列优化 DP | 12 | 1696 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十一、优化 DP / §11.4 树状数组/线段树优化 DP | 8 | Reference only |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十一、优化 DP / §11.5 字典树优化 DP | 4 | 139 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十一、优化 DP / §11.6 矩阵快速幂优化 DP | 13 | 70, 509, 790 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十一、优化 DP / §11.7 斜率优化 DP | 4 | Reference only |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十一、优化 DP / §11.8 WQS 二分优化 DP | 7 | Reference only |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十一、优化 DP / §11.9 其他优化 DP | 13 | Reference only |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十二、树形 DP / §12.1 树的直径 | 12 | 543, 124 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十二、树形 DP / §12.2 树上最大独立集 | 5 | 337 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十二、树形 DP / §12.3 树上最小支配集 | 1 | 968 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十二、树形 DP / §12.4 换根 DP | 8 | 834 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十二、树形 DP / §12.5 其他树形 DP | 8 | Reference only |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十三、图 DP | 13 | 787 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十四、博弈 DP | 13 | 486 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 十五、概率 DP、期望 DP | 5 | 688 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 专题：输出具体方案（打印方案） | 13 | 1092 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 专题：前后缀分解 | 63 | 238, 42 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 专题：跳跃游戏 | 10 | 1696 |
| [tXLS3i](https://leetcode.cn/circle/discuss/tXLS3i/) | 其他 | 7 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 零、常用枚举技巧 / §0.1 枚举右，维护左 | 1 | 1 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 零、常用枚举技巧 / §0.1 枚举右，维护左 / §0.1.1 基础 | 26 | 1 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 零、常用枚举技巧 / §0.1 枚举右，维护左 / §0.1.2 进阶 | 21 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 零、常用枚举技巧 / §0.2 枚举中间 / §0.2.1 基础 | 3 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 零、常用枚举技巧 / §0.2 枚举中间 / §0.2.2 进阶 | 11 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 零、常用枚举技巧 / §0.3 遍历对角线 | 6 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 一、前缀和 / §1.1 基础 | 13 | 53 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 一、前缀和 / §1.2 前缀和与哈希表 | 35 | 560, 974, 437 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 一、前缀和 / §1.3 距离和 | 8 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 一、前缀和 / §1.4 状态压缩前缀和 | 5 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 一、前缀和 / §1.5 进阶 | 21 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 一、前缀和 / §1.6 二维前缀和 | 7 | 1314 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 二、差分 / §2.1 一维差分 | 1 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 二、差分 / §2.1 一维差分 / §2.1.1 基础 | 9 | 1109 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 二、差分 / §2.1 一维差分 / §2.1.2 进阶 | 33 | 56, 732, 2406 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 二、差分 / §2.2 二维差分 | 4 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 三、栈 / §3.1 基础 | 8 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 三、栈 / §3.2 进阶 | 10 | 155 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 三、栈 / §3.3 邻项消除 | 16 | 1047 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 三、栈 / §3.4 合法括号字符串（RBS） | 13 | 20 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 三、栈 / §3.5 表达式解析 | 20 | 394, 227 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 三、栈 / §3.6 对顶栈 | 1 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 四、队列 / §4.1 基础 | 10 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 四、队列 / §4.2 设计 | 6 | 232, 622 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 四、队列 / §4.3 双端队列 | 2 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 四、队列 / §4.4 单调队列 | 8 | 239, 862 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 五、堆（优先队列） / §5.1 基础 | 22 | 2406 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 五、堆（优先队列） / §5.2 进阶 | 33 | 1631, 1235 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 五、堆（优先队列） / §5.3 第 K 小/大 | 8 | 378, 373 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 五、堆（优先队列） / §5.4 重排元素 | 7 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 五、堆（优先队列） / §5.5 反悔堆 | 10 | 630 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 五、堆（优先队列） / §5.6 懒删除堆 | 14 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 五、堆（优先队列） / §5.7 对顶堆（动态第 K 小/大） | 11 | 295 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 六、字典树（trie） / §6.1 基础 | 13 | 208 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 六、字典树（trie） / §6.2 进阶 | 18 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 六、字典树（trie） / §6.3 字典树优化 DP | 4 | 139 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 六、字典树（trie） / §6.4 0-1 字典树（异或字典树） | 8 | 421 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 七、并查集 / §7.1 基础 | 8 | 684 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 七、并查集 / §7.2 进阶 | 26 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 七、并查集 / §7.3 中介并查集 | 9 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 七、并查集 / §7.4 数组上的并查集 | 7 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 七、并查集 / §7.5 区间并查集 | 3 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 七、并查集 / §7.6 带权并查集（边权并查集） | 4 | 399 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 八、树状数组和线段树 | 1 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 八、树状数组和线段树 / §8.1 树状数组 | 33 | 307 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 八、树状数组和线段树 / §8.2 逆序对 | 10 | 315 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 八、树状数组和线段树 / §8.3 线段树（无区间更新） | 17 | 104 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 八、树状数组和线段树 / §8.4 Lazy 线段树（有区间更新） | 10 | 2569 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 八、树状数组和线段树 / §8.5 动态开点线段树 | 7 | 732 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 八、树状数组和线段树 / §8.6 可持久化线段树 | 1 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 八、树状数组和线段树 / §8.7 ST 表（Sparse Table） | 3 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 九、伸展树（Splay 树） | 2 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 十、根号算法 / §10.1 分块 | 2 | 307 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 十、根号算法 / §10.2 莫队算法 | 4 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 十、根号算法 / §10.3 根号分解（Sqrt Decomposition） | 3 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 十、根号算法 / §10.4 其他 | 1 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 专题：离线算法 | 14 | 1697 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 编程能力强化训练 / Part A | 7 | Reference only |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 编程能力强化训练 / Part B | 4 | 146, 460 |
| [mOr1u6](https://leetcode.cn/circle/discuss/mOr1u6/) | 编程能力强化训练 / Part C | 3 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 一、数论 / §1.1 判断质数 | 6 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 一、数论 / §1.2 预处理质数（筛质数） | 11 | 204 |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 一、数论 / §1.3 质因数分解 | 14 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 一、数论 / §1.4 阶乘分解 | 2 | 172 |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 一、数论 / §1.5 因子 | 18 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 一、数论 / §1.6 最大公约数（GCD） | 25 | 1071 |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 一、数论 / §1.7 最小公倍数（LCM） | 5 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 一、数论 / §1.8 互质 | 4 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 一、数论 / §1.9 同余 | 3 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 一、数论 / §1.10 数论分块 | 1 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 一、数论 / §1.11 莫比乌斯函数 | 2 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 一、数论 / §1.12 其他 | 9 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 二、组合数学 / §2.1 乘法原理 | 14 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 二、组合数学 / §2.2 组合计数 | 43 | 62 |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 二、组合数学 / §2.3 容斥原理 | 14 | 1201 |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 二、组合数学 / §2.4 生成函数（母函数） | 7 | 629 |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 三、概率期望 | 7 | 688 |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 四、博弈论 | 24 | 292, 486 |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 五、计算几何 / §5.1 点、线 | 4 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 五、计算几何 / §5.2 圆 | 4 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 五、计算几何 / §5.3 矩形、多边形 | 7 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 五、计算几何 / §5.4 凸包 | 2 | 587 |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 五、计算几何 / §5.5 其他 | 1 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 六、随机算法 / §6.1 随机数 | 11 | 398, 384, 380, 528, 470 |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 六、随机算法 / §6.2 随机化技巧 | 5 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 六、随机算法 / §6.3 异或哈希（XOR hashing） | 1 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 七、杂项 / §7.1 回文数 | 14 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 七、杂项 / §7.2 整数拆分 | 2 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 七、杂项 / §7.3 曼哈顿距离与切比雪夫距离 | 8 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 七、杂项 / §7.4 卷积 | 8 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 七、杂项 / §7.5 快速沃尔什变换（FWT） | 2 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 七、杂项 / §7.6 拉格朗日插值 | 1 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 七、杂项 / §7.8 摩尔投票法 | 5 | 169 |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 七、杂项 / §7.9 确定数位 | 2 | Reference only |
| [IYT3ss](https://leetcode.cn/circle/discuss/IYT3ss/) | 七、杂项 / §7.10 其他 | 43 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 一、贪心策略 / §1.1 从最小/最大开始贪心 | 57 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 一、贪心策略 / §1.2 单序列配对 | 5 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 一、贪心策略 / §1.3 双序列配对 | 11 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 一、贪心策略 / §1.4 从最左/最右开始贪心 | 28 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 一、贪心策略 / §1.5 划分型贪心 | 9 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 一、贪心策略 / §1.6 先枚举，再贪心 | 6 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 一、贪心策略 / §1.7 交换论证法 | 12 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 一、贪心策略 / §1.8 相邻不同 | 15 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 一、贪心策略 / §1.9 反悔贪心 | 8 | 630 |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 二、区间贪心 / §2.1 不相交区间 | 4 | 435 |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 二、区间贪心 / §2.2 区间分组 | 2 | 2406 |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 二、区间贪心 / §2.3 区间选点 | 3 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 二、区间贪心 / §2.4 区间覆盖 | 3 | 45, 1024 |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 二、区间贪心 / §2.5 合并区间 | 18 | 56, 55, 763 |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 二、区间贪心 / §2.6 其他区间贪心 | 4 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 三、字符串贪心 / §3.1 字典序最小/最大 | 38 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 三、字符串贪心 / §3.2 回文串贪心 | 18 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 四、数学贪心 / §4.1 基础 | 7 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 四、数学贪心 / §4.2 乘积贪心 | 3 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 四、数学贪心 / §4.3 排序不等式 | 11 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 四、数学贪心 / §4.4 均值不等式 | 5 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 四、数学贪心 / §4.5 中位数贪心 | 13 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 四、数学贪心 / §4.6 归纳法 | 3 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 四、数学贪心 / §4.7 其他数学贪心 | 4 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 五、思维题 / §5.1 从特殊到一般 | 14 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 五、思维题 / §5.2 脑筋急转弯 | 57 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 五、思维题 / §5.3 等价转化 | 16 | 49 |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 五、思维题 / §5.4 逆向思维 | 28 | 417 |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 五、思维题 / §5.5 贡献法 | 13 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 五、思维题 / §5.6 两次扫描 | 4 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 五、思维题 / §5.7 交换元素 | 4 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 五、思维题 / §5.8 分类讨论 | 49 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 六、构造题 | 27 | Reference only |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 七、交互题 | 20 | 374 |
| [g6KTKL](https://leetcode.cn/circle/discuss/g6KTKL/) | 八、其他 | 21 | 134 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 一、链表 / §1.1 遍历链表 | 9 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 一、链表 / §1.2 删除节点 | 8 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 一、链表 / §1.3 插入节点 | 4 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 一、链表 / §1.4 反转链表 | 5 | 206, 25 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 一、链表 / §1.5 前后指针 | 3 | 19 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 一、链表 / §1.6 快慢指针 | 12 | 234, 141 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 一、链表 / §1.7 双指针 | 3 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 一、链表 / §1.8 合并链表 | 6 | 21 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 一、链表 / §1.9 分治 | 2 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 一、链表 / §1.10 综合应用 | 7 | 146, 460 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 一、链表 / §1.11 其他 | 5 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 二、二叉树 / §2.1 遍历二叉树 | 9 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 二、二叉树 / §2.2 自顶向下 DFS（先序遍历） | 17 | 104 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 二、二叉树 / §2.3 自底向上 DFS（后序遍历） | 34 | 104 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 二、二叉树 / §2.4 自底向上 DFS：删点 | 3 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 二、二叉树 / §2.5 有递有归 | 4 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 二、二叉树 / §2.6 二叉树的直径 | 5 | 543, 124 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 二、二叉树 / §2.7 回溯 | 5 | 437 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 二、二叉树 / §2.8 最近公共祖先 | 9 | 236 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 二、二叉树 / §2.9 二叉搜索树 | 20 | 230, 98 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 二、二叉树 / §2.10 创建二叉树 | 13 | 105 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 二、二叉树 / §2.11 插入/删除节点 | 5 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 二、二叉树 / §2.12 树形 DP | 3 | 337, 968 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 二、二叉树 / §2.13 二叉树 BFS | 26 | 102 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 二、二叉树 / §2.14 链表+二叉树 | 6 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 二、二叉树 / §2.15 N 叉树 | 11 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 二、二叉树 / §2.16 其他 | 23 | 297 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 三、一般树 / §3.1 遍历 | 3 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 三、一般树 / §3.2 自顶向下 DFS | 13 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 三、一般树 / §3.3 自底向上 DFS | 12 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 三、一般树 / §3.4 有递有归 | 2 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 三、一般树 / §3.5 树的直径 | 7 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 三、一般树 / §3.6 树的拓扑排序 | 3 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 三、一般树 / §3.7 DFS 时间戳 | 4 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 三、一般树 / §3.8 最近公共祖先（LCA）、倍增算法 | 12 | 1483 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 三、一般树 / §3.9 虚树 | 1 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 三、一般树 / §3.10 树上启发式合并 | 3 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 三、一般树 / §3.11 点分治 | 1 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 三、一般树 / §3.12 树上滑动窗口 | 2 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 三、一般树 / §3.13 其他 | 4 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 四、回溯 / §4.1 入门回溯 | 1 | Reference only |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 四、回溯 / §4.2 子集型回溯 | 22 | 78, 39 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 四、回溯 / §4.3 划分型回溯 | 7 | 131 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 四、回溯 / §4.4 组合型回溯 | 5 | 22 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 四、回溯 / §4.5 排列型回溯 | 11 | 46, 52, 37 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 四、回溯 / §4.6 有重复元素的回溯 | 7 | 40 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 四、回溯 / §4.7 搜索 | 30 | 79 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 四、回溯 / §4.8 折半搜索 | 10 | 494, 1755 |
| [K0n2gO](https://leetcode.cn/circle/discuss/K0n2gO/) | 五、其他递归/分治 | 9 | 215, 912 |
| [SJFwQI](https://leetcode.cn/circle/discuss/SJFwQI/) | 一、KMP（前缀的后缀） | 16 | 28 |
| [SJFwQI](https://leetcode.cn/circle/discuss/SJFwQI/) | 二、Z 函数（后缀的前缀） | 11 | 28, 2223 |
| [SJFwQI](https://leetcode.cn/circle/discuss/SJFwQI/) | 三、Manacher 算法（回文串） | 12 | 5 |
| [SJFwQI](https://leetcode.cn/circle/discuss/SJFwQI/) | 四、字符串哈希 | 19 | 28, 187, 1044 |
| [SJFwQI](https://leetcode.cn/circle/discuss/SJFwQI/) | 五、最小表示法 | 7 | 899 |
| [SJFwQI](https://leetcode.cn/circle/discuss/SJFwQI/) | 七、AC 自动机 | 7 | Reference only |
| [SJFwQI](https://leetcode.cn/circle/discuss/SJFwQI/) | 八、后缀数组/后缀自动机 | 20 | 1044 |
| [SJFwQI](https://leetcode.cn/circle/discuss/SJFwQI/) | 九、子序列自动机 | 6 | 792 |
| [SJFwQI](https://leetcode.cn/circle/discuss/SJFwQI/) | 十、其他 | 3 | Reference only |
