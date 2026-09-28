# Problem-to-practice coverage audit

Audit of the checked-in snapshots on 2026-09-27. The source of truth for problem IDs and topic metadata is `packages/content/catalog.json`; guide membership comes from `packages/content/reference-index.json`. The official topic snapshot is `packages/content/official-tags.json`. Guide sections are source-backed practice groupings, while topic collections are metadata groupings. Neither association proves that a particular community implementation uses the named technique.

| Measure | Count |
|---|---:|
| Catalog problems | 4,068 |
| Catalog problems with at least one topic tag | 3,629 |
| Distinct topic slugs present on those problems | 172 |
| Distinct topic slugs routed to a practice collection after this change | 172 |
| Source guides / problem-bearing sections | 12 / 313 |
| Source-section memberships / unique problem IDs | 3,582 / 2,732 |
| Source-section IDs absent from the catalog | 0 |
| Catalog problems without topic metadata | 439 |
| Untagged catalog problems with a source-section association | 6 |
| Untagged catalog problems without either association | 433 |
| Community solution cards without a tag or source association | 22 |

The previous topic router recognized 62 of the 172 slugs in this catalog. `scripts/content/practice.py` now routes the remaining fine-grained slugs into the twelve existing broad curriculum roots and creates a topic collection for each slug that occurs. This is a navigation improvement: it does not add authored solutions, convert reference-only catalog entries into worked cards, or claim that an imported implementation follows a guide technique. Existing `topic-<slug>` and `practice-<source>-<index>` IDs remain stable. The 22 otherwise unclassified community cards now explicitly carry their fallback collection ID.

The 313 guide section IDs and their English paths remain unchanged. The source index supplies all 3,582 problem associations, so inventing extra section memberships from a broad tag would make the taxonomy less trustworthy. The original source outline is [EndlessCheng's algorithm directory](https://github.com/EndlessCheng/codeforces-go); [LeetCode's problemset](https://leetcode.com/problemset/) is the canonical destination for problem statements and topic browsing. No guide prose or solutions were copied for this audit.

## Remaining work

- The 433 untagged, unreferenced catalog entries have no justified placement in a specific practice group. They remain factual catalog references; metadata refresh or individual editorial review is needed before assigning a pattern.
- A topic collection is wider than a pattern leaf. Fine-grained slugs now make specialist areas such as flow, matching, suffix automata, persistent structures, and advanced number theory discoverable, but these collections do not constitute new authored lessons.
- The checked-in catalog and guide are dated snapshots. New LeetCode problems or changed tags require a new source refresh and audit; no finite snapshot can prove literal exhaustiveness of all future problems or techniques.
- Specialist extensions already identified in [COVERAGE.md](COVERAGE.md), including heavy-light decomposition, Mo's algorithm, maximum flow, convolution transforms, and generating functions, still need independently authored explanations and validated implementations before they can be counted as worked pattern lessons.

To reproduce the fixed-input counts, count catalog entries and distinct `tags[].slug` values, then count `sections[].problemIds` across the twelve reference sources. Count an unassociated catalog entry only when it has neither a tag nor membership in a source section. A card with no such association can be placed in the clearly labeled fallback collection without attributing a technique to it.
