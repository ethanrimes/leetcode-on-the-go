# Foundations coverage audit

Reviewed 2026-09-27 against [labuladong's algorithm roadmap](https://labuladong.online/en/roadmap/algo/), its [algorithm summary](https://labuladong.online/en/algo/essential-technique/algorithm-summary/) and [binary-tree traversal guide](https://labuladong.online/en/algo/data-structure-basic/binary-tree-traverse-basic/), plus LeetCode's official [binary search](https://leetcode.com/tag/binary-search/), [sliding window](https://leetcode.com/tag/sliding-window/), [monotonic stack](https://leetcode.com/tag/monotonic-stack/), [tree](https://leetcode.com/tag/tree/), and [string](https://leetcode.com/tag/string/) topic lists. LeetCode's public topic pages expose tag membership but not a fine-grained teaching taxonomy; the subdivisions below are editorial, grounded in distinct invariants and official problems.

## Added authored lessons

| Family | Newly explicit decision rule | LeetCode anchor |
|---|---|---|
| Binary search | First/last occurrence via two lower bounds | [34](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) |
| Binary search | Rotated-array minimum by comparing against right boundary | [153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) |
| Sliding window | Shrink a positive-sum interval to minimum length | [209](https://leetcode.com/problems/minimum-size-subarray-sum/) |
| Prefix state | Save the earliest equal balance for a longest binary interval | [525](https://leetcode.com/problems/contiguous-array/) |
| Monotone stack | Scan a circular array twice, inserting candidates once | [503](https://leetcode.com/problems/next-greater-element-ii/) |
| Monotone stack | Remove larger preceding digits under a deletion budget | [402](https://leetcode.com/problems/remove-k-digits/) |
| String parsing | Normalize whitespace, then reorder tokens | [151](https://leetcode.com/problems/reverse-words-in-a-string/) |
| String parsing | Compare dotted numeric components with zero padding | [165](https://leetcode.com/problems/compare-version-numbers/) |
| Trees | Choose the last node in each BFS level for the right view | [199](https://leetcode.com/problems/binary-tree-right-side-view/) |
| Trees | Compare crossed child pairs for mirror symmetry | [101](https://leetcode.com/problems/symmetric-tree/) |
| Linked lists | Fast/slow midpoint, explicitly choosing the second middle | [876](https://leetcode.com/problems/middle-of-the-linked-list/) |

All new lessons have original explanations and Python solutions. Existing node IDs and mappings are unchanged. [42. Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) was already an authored lesson in `completion.py`, so the audit did not create a duplicate card.

## Remaining distinctions

This is broader foundation coverage, not a claim of literal exhaustiveness. The authored catalog still has fewer dedicated lessons for matrix search across differently sorted layouts ([74](https://leetcode.com/problems/search-a-2d-matrix/), [240](https://leetcode.com/problems/search-a-2d-matrix-ii/)); fixed-length frequency windows ([438](https://leetcode.com/problems/find-all-anagrams-in-a-string/)); streaming heap interfaces ([703](https://leetcode.com/problems/kth-largest-element-in-a-stream/)); BST deletion ([450](https://leetcode.com/problems/delete-node-in-a-bst/)); and linked-list intersection/cycle entry ([160](https://leetcode.com/problems/intersection-of-two-linked-lists/), [142](https://leetcode.com/problems/linked-list-cycle-ii/)). Some may already appear as attributed practice problems or official-topic references. A worked lesson requires an authored invariant, code, and validated example, not merely a topic tag or source-guide membership.
