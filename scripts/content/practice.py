"""Expand source-backed practice collections and licensed community study cards."""
import hashlib
import json
from collections import defaultdict
from .practice_paths import PATHS
from .base import ROOT

ROOTS = {'0viNMK':'two-pointers-windows','SqopEo':'binary-search','9oZFK9':'stacks-heaps-range-queries','YiXPXW':'graphs-grids','dHn9Vk':'bits-math-geometry','01LUak':'graphs-grids','tXLS3i':'dynamic-programming','mOr1u6':'stacks-heaps-range-queries','IYT3ss':'bits-math-geometry','g6KTKL':'greedy-intervals','K0n2gO':'trees-linked-lists','SJFwQI':'strings-tries'}
TAG_ROOTS = {
'dynamic-programming':'dynamic-programming','binary-search':'binary-search','two-pointers':'two-pointers-windows','sliding-window':'two-pointers-windows',
'depth-first-search':'graphs-grids','breadth-first-search':'graphs-grids','graph':'graphs-grids','union-find':'graphs-grids','topological-sort':'graphs-grids','shortest-path':'graphs-grids','minimum-spanning-tree':'graphs-grids','biconnected-component':'graphs-grids','strongly-connected-component':'graphs-grids','eulerian-circuit':'graphs-grids','matrix':'graphs-grids',
'binary-tree':'trees-linked-lists','tree':'trees-linked-lists','binary-search-tree':'trees-linked-lists','linked-list':'trees-linked-lists',
'backtracking':'backtracking-enumeration','enumeration':'backtracking-enumeration','recursion':'backtracking-enumeration','divide-and-conquer':'backtracking-enumeration','meet-in-the-middle':'backtracking-enumeration',
'stack':'stacks-heaps-range-queries','monotonic-stack':'stacks-heaps-range-queries','monotonic-queue':'stacks-heaps-range-queries','queue':'stacks-heaps-range-queries','heap-priority-queue':'stacks-heaps-range-queries','segment-tree':'stacks-heaps-range-queries','binary-indexed-tree':'stacks-heaps-range-queries','ordered-set':'stacks-heaps-range-queries','design':'stacks-heaps-range-queries',
'string':'strings-tries','trie':'strings-tries','string-matching':'strings-tries','rolling-hash':'strings-tries','suffix-array':'strings-tries',
'greedy':'greedy-intervals','sorting':'sorting-selection','quickselect':'sorting-selection','bucket-sort':'sorting-selection','radix-sort':'sorting-selection','merge-sort':'sorting-selection','counting-sort':'sorting-selection',
'math':'bits-math-geometry','bit-manipulation':'bits-math-geometry','bitmask':'bits-math-geometry','number-theory':'bits-math-geometry','combinatorics':'bits-math-geometry','geometry':'bits-math-geometry','probability-and-statistics':'bits-math-geometry','randomized':'bits-math-geometry','game-theory':'bits-math-geometry','rejection-sampling':'bits-math-geometry','reservoir-sampling':'bits-math-geometry',
'array':'arrays-hashing','hash-table':'arrays-hashing','prefix-sum':'arrays-hashing','counting':'arrays-hashing','simulation':'arrays-hashing','hash-function':'arrays-hashing'
}
# The catalog snapshot includes finer-grained topic slugs than the 75 broad
# official topics. Route these to *topic collections*, never to authored
# pattern leaves: a tag describes a problem, not the checked-in solution.
TAG_ROOTS.update({tag: root for root, tags in {
    'arrays-hashing': '''data-stream hash-function''',
    'greedy-intervals': '''boyer-moore-majority-vote-algorithm sweep-line interactive''',
    'binary-search': '''ternary-search''',
    'dynamic-programming': '''0-1-knapsack complete-knapsack dp-on-trees knapsack-problem longest-common-subsequence longest-increasing-subsequence memoization mixed-knapsack multiple-knapsack''',
    'graphs-grids': '''0-1-bfs a-search articulation-point bellman-ford-algorithm bidirectional-search bipartite-graph boruvkas-algorithm bridge-graph dijkstra dinics-algorithm directed-acyclic-graph edmonds-karp-algorithm eulerian-graph eulerian-path flow-network floyd-warshall-algorithm graph-coloring hamiltonian-path heuristic-search hungarian-algorithm k-shortest-path kosarajus-algorithm kruskals-algorithm matching-graph maximum-flow maximum-matching minimum-cost-flow minimum-cut mpm-algorithm perfect-matching planar-graph prims-algorithm push-relabel-algorithm semi-eulerian-graph successive-shortest-path-algorithm tarjans-scc-algorithm''',
    'trees-linked-lists': '''binary-lifting cartesian-tree doubly-linked-list floyds-cycle-finding-algorithm lowest-common-ancestor''',
    'stacks-heaps-range-queries': '''bracket-sequences heap iterator k-d-tree li-chao-tree persistent-data-structure range-minimum-maximum-query sparse-table splay-tree sqrt-decomposition treap''',
    'backtracking-enumeration': '''algorithm-x brute-force-search dancing-links''',
    'strings-tries': '''aho-corasick-algorithm boyer-moore-string-search-algorithm knuth-morris-pratt-algorithm lexicographically-minimal-string-rotation lyndon-factorization manacher palindromic-tree suffix-automaton suffix-tree z-algorithm''',
    'sorting-selection': '''bubble-sort quicksort sort timsort tournament-sort''',
    'bits-math-geometry': '''bezouts-lemma brainteaser convex-hull euclidean-algorithm eulers-theorem eulers-totient-function extended-euclidean-algorithm fermats-little-theorem greatest-common-divisor impartial-game inclusion-exclusion-principle least-common-multiple linear-algebra minimax-algorithm minimum-enclosing-circle newtons-method nim-game pigeonhole-principle polygons primality-test prime-factorization prime-number-sieve sieve-theory sprague-grundy-theorem triangulation zero-sum-game''',
}.items() for tag in tags.split()})

def expand(nodes, problems, reference):
    catalog=json.loads((ROOT/'packages/content/catalog.json').read_text())['problems']
    catalog_by_id={p['id']:p for p in catalog}
    community=json.loads((ROOT/'packages/content/community-solutions.json').read_text())
    node_by_id={n['id']:n for n in nodes}
    memberships=defaultdict(list)
    def add(id, parent, title, kind='category', ids=(), url='', original=''):
        if id in node_by_id: return
        node=dict(id=id,parentId=parent,title=title,kind=kind,level='Advanced' if any(w in title.lower() for w in ['advanced','persistent','convex hull','flow','wqs','mobius','centroid']) else 'Intermediate',priority='Useful',
                  description=('Source-indexed problems grouped by '+title.lower()+'.') if kind=='collection' else 'Explore practice sets organized by technique.',
                  approach='Read the official problem statement, identify a useful state or invariant, then draft your solution. Reveal the implementation to compare your reasoning. This is a practice grouping; a community implementation may use a different technique from the source guide.',
                  tips=['Compare multiple approaches before deciding which invariant to remember.','Use difficulty sorting to progress from easier problems to harder variations.'],
                  why='Broaden transfer beyond one example by practicing different problems from the same source grouping.',
                  sourceUrls=[url] if url else [],references=[],problemIds=[p for p in ids if p in catalog_by_id],sourceTitle=original)
        nodes.append(node);node_by_id[id]=node
        for pid in node['problemIds']: memberships[pid].append(id)
    for source in reference['sources']:
        paths=PATHS[source['id']]
        assert len(paths)==len(source['sections']), source['id']
        for index,(section,path) in enumerate(zip(source['sections'],paths)):
            root=ROOTS[source['id']]
            if source['id']=='mOr1u6' and index<=15: root='arrays-hashing'
            if source['id']=='mOr1u6' and 33<=index<=36: root='strings-tries'
            if source['id']=='mOr1u6' and 37<=index<=42: root='graphs-grids'
            if source['id']=='K0n2gO' and index>=40: root='backtracking-enumeration'
            parent=root+'-practice'
            add(parent,root,'Extended practice',url=source['url'])
            for depth,title in enumerate(path[:-1]):
                id='practice-group-'+hashlib.sha1((root+source['id']+'/'.join(path[:depth+1])).encode()).hexdigest()[:12]
                add(id,parent,title,url=source['url']);parent=id
            add(f'practice-{source["id"]}-{index}',parent,path[-1],'collection',section['problemIds'],source['url'],' / '.join(section['path']))
    # Official topic tags are broad groupings, kept distinct from individual patterns.
    by_tag=defaultdict(list); tag_names={}
    for p in catalog:
        for tag in p.get('tags',[]):
            if tag['slug'] in TAG_ROOTS: by_tag[tag['slug']].append(p['id']);tag_names[tag['slug']]=tag['name']
    for tag,ids in sorted(by_tag.items()):
        root=TAG_ROOTS[tag];parent=root+'-official-topics'
        add(parent,root,'Official topic collections')
        add('topic-'+tag,parent,tag_names[tag]+' practice','collection',ids,'https://leetcode.com/tag/'+tag+'/')
    add('community-unclassified','arrays-hashing','Unclassified community problems','collection',[],community['repository'])
    for problem in problems.values():
        problem['origin']='authored';problem['collectionIds']=memberships[problem['id']]
    imported=0
    for record in community['problems']:
        pid=record['id']
        if pid in problems: continue  # Authored lessons remain the canonical lesson for their IDs.
        metadata=catalog_by_id[pid]
        collections=memberships[pid]
        primary=collections[0] if collections else 'community-unclassified'
        if not collections:
            node_by_id[primary]['problemIds'].append(pid)
            collections=[primary]
        solutions=[]
        for i,variant in enumerate(record['solutions']):
            solutions.append(dict(patternId=primary,title='Community implementation'+(f' {i+1}' if len(record['solutions'])>1 else ''),language='Python',
                                  approach='Reference implementation by Peng-Yu Chen (walkccc). Read the code to identify its invariant and derive its time and space bounds. Source grouping does not guarantee that this implementation uses that exact pattern.',
                                  code=variant['code'],time='Not independently annotated',space='Not independently annotated',
                                  attribution=dict(author=community['author'],license='MIT',url=variant['url'],commit=community['commit'],sha256=variant['sha256'])))
        problems[pid]=dict(**metadata,origin='community',collectionIds=collections,patternIds=[primary],
                           description='Read the official statement for '+metadata['title']+' on LeetCode, then use this workspace to draft and recall the solution. This card includes an attributed community implementation; the full statement and examples remain on LeetCode.',
                           examples=[],constraints='The draft preserves the source implementation’s public method signatures. Refer to LeetCode for constraints, required node types, imports, and execution.',
                           starter=record['starter'],sourceUrl='https://leetcode.com/problems/'+metadata['slug']+'/',solutions=solutions)
        imported+=1
    # Explicit source-section associations for related practice at each original pattern leaf.
    for node in nodes:
        if node['kind']=='pattern': node['problemIds']=sorted({pid for r in node['references'] for pid in r['problemIds'] if pid in catalog_by_id},key=int)
    return catalog,dict(authoredProblems=sum(p['origin']=='authored' for p in problems.values()),communityProblems=imported,sourceCollections=sum(n['kind']=='collection' and n['id'].startswith('practice-') for n in nodes),communityCommit=community['commit'])
