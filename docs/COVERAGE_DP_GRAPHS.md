# DP and graph coverage audit

Reviewed 2026-09-27. This audit concerns **authored worked patterns** in `scripts/content/dynamic_programming.py` and `scripts/content/graphs.py`. The broader catalog and attributed practice collections already contain many more problem links; a catalog link is not a worked lesson.

## Sources and comparison

- [EndlessCheng's algorithm index](https://github.com/EndlessCheng/codeforces-go/blob/master/README.md) distinguishes knapsack, interval/subset/digit/tree DP, transition optimizations, and graph algorithms including shortest paths, MST, low-link structure, matching, and flow. This is a living contest-oriented index, not a finite checklist of all possible patterns.
- [EndlessCheng's graph templates](https://github.com/EndlessCheng/codeforces-go/blob/master/copypasta/graph.go) make the finer graph variants explicit. The current curriculum already had Dijkstra, 0-1 BFS, bounded-edge Bellman–Ford, Floyd–Warshall, minimax paths, bridges, and Eulerian paths.
- [Labuladong's core problem set](https://labuladong.online/en/problemset/core/) separates grid flood fill, unit-cost maze BFS, graph cycle/order/connectivity, MST, weighted shortest paths, and 0-1/unbounded/group knapsack. [Its DP exercise set](https://labuladong.online/en/algo/problem-set/dynamic-programming-i/) includes obstacle grids, divisibility states, and divisible subset reconstruction among its examples.
- LeetCode's official problem statements anchor the precise contracts, including [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) and [Path with Maximum Probability](https://leetcode.com/problems/path-with-maximum-probability/).

## Authored additions

| Area | New pattern distinction | LeetCode ID |
|---|---|---:|
| DP | Grid paths whose obstacles zero out reachable state | [63](https://leetcode.com/problems/unique-paths-ii/) |
| DP | Contiguous matching suffix versus subsequence matching | [718](https://leetcode.com/problems/maximum-length-of-repeated-subarray/) |
| DP | Maximize a sum by a small remainder state | [1262](https://leetcode.com/problems/greatest-sum-divisible-by-three/) |
| DP | Recover an optimal divisible chain via predecessors | [368](https://leetcode.com/problems/largest-divisible-subset/) |
| DP | Stock state machine with a bounded count of completed trades | [188](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/) |
| Graph | Mark boundary-connected cells before capturing interior regions | [130](https://leetcode.com/problems/surrounded-regions/) |
| Graph | Ordinary BFS for eight-direction unit-cost grid paths | [1091](https://leetcode.com/problems/shortest-path-in-binary-matrix/) |
| Graph | Construct a topological ordering, versus only detect feasibility | [210](https://leetcode.com/problems/course-schedule-ii/) |
| Graph | Count components by unioning an adjacency matrix | [547](https://leetcode.com/problems/number-of-provinces/) |
| Graph | Maximize a multiplicative path value with a heap | [1514](https://leetcode.com/problems/path-with-maximum-probability/) |

These are separate reusable transitions, not a claim that every new problem needs its own pattern. Each added card has an original recognition cue, recurrence or invariant, pitfall, and Python implementation.

## Remaining gaps and limits

The authored DP set still has no full worked lesson for bounded/group knapsack, tree knapsack, divide-and-conquer optimization, convex-hull-trick optimization, WQS binary search, or SOS transforms. The authored graph set still lacks worked matching, max-flow/min-cost-flow, biconnected decomposition, and specialized shortest-path variants such as Johnson's algorithm. Some of these have references or community solutions elsewhere in the product; they should not be counted as authored coverage until the underlying invariant and implementation are reviewed. Coverage cannot be literally exhaustive because the cited guides continue to evolve and problem modeling can generate new combinations of familiar techniques.

The added files passed Python syntax checks, and each new implementation matched its authored example. The examples are smoke checks, not proof of correctness for all input constraints. Generated content was intentionally left for the parent build pipeline.
