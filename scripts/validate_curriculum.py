"""Check graph integrity and execute authored solution examples (not a user-code judge)."""
import ast
import copy
import hashlib
import json
import math
from pathlib import Path
from types import SimpleNamespace
from collections import deque

root=Path(__file__).resolve().parents[1]
data=json.loads((root/'packages/content/curriculum.json').read_text())
nodes={n['id']:n for n in data['nodes']}
assert len(nodes)==len(data['nodes']), 'Duplicate node IDs'
for node in nodes.values():
    seen=set(); current=node
    while current['parentId']:
        assert current['id'] not in seen, 'Taxonomy cycle'
        seen.add(current['id']); current=nodes[current['parentId']]
    assert all(node.get(k) for k in ['description','approach','tips','level','priority']), node['id']

def tree(values):
    if not values or values[0] is None: return None
    first=SimpleNamespace(val=values[0],left=None,right=None); q=deque([first]); i=1
    while q and i<len(values):
        node=q.popleft()
        for side in ('left','right'):
            if i<len(values) and values[i] is not None:
                child=SimpleNamespace(val=values[i],left=None,right=None); setattr(node,side,child); q.append(child)
            i+=1
    return first

def linked(values):
    dummy=SimpleNamespace(next=None); tail=dummy
    for value in values: tail.next=SimpleNamespace(val=value,next=None); tail=tail.next
    return dummy.next

errors=[]; checked=0
for problem in data['problems']:
    assert problem['solutions']
    if problem.get('origin') == 'community':
        assert not problem.get('test'), 'Imported code must never execute in authored validation'
        for solution in problem['solutions']:
            ast.parse(solution['code'])
            assert solution['patternId'] in nodes
            credit=solution['attribution']
            assert credit['license']=='MIT' and credit['url'].startswith('https://github.com/walkccc/LeetCode/blob/'+credit['commit']+'/')
            assert hashlib.sha256(solution['code'].encode()).hexdigest()==credit['sha256']
        continue
    assert problem['examples']
    assert len(set(problem['patternIds']))==len(problem['patternIds'])
    for solution in problem['solutions']:
        assert solution['patternId'] in nodes
        assert solution['patternId'] in problem['patternIds']
        code=solution['code']; ast.parse(code); scope={}; exec(compile(code,'<authored-curriculum>','exec'),scope)
        args=copy.deepcopy(problem['test']['args']); adapter=problem['test'].get('adapter')
        if adapter=='tree': args[0]=tree(args[0])
        if adapter in ('linked','linked-bool'): args=[linked(v) if isinstance(v,list) else v for v in args]
        if adapter=='cycle':
            values,pos=args; head=linked(values); chain=[]; node=head
            while node: chain.append(node); node=node.next
            if chain and pos>=0: chain[-1].next=chain[pos]
            args=[head]
        try:
            actual=scope['solve'](*args)
            if adapter=='linked':
                values=[]
                while actual: values.append(actual.val); actual=actual.next
                actual=values
            if adapter=='tree-output':
                q=deque([actual]); values=[]
                while q:
                    node=q.popleft(); values.append(node.val if node else None)
                    if node: q.extend([node.left,node.right])
                while values and values[-1] is None: values.pop()
                actual=values
            expected=problem['test']['expected']
            comparison=problem['test'].get('comparison')
            if comparison=='rand10': assert isinstance(actual,int) and 1<=actual<=10
            elif comparison=='permutation': assert sorted(actual)==sorted(expected)
            else: assert actual==expected or (isinstance(actual,float) and isinstance(expected,(int,float)) and math.isclose(actual,expected)), f'{actual!r} != {expected!r}'
            checked+=1
        except Exception as exc: errors.append(f'{problem["id"]} / {solution["title"]}: {exc}')
for node in nodes.values():
    if node['kind']=='pattern': assert any(node['id'] in p['patternIds'] for p in data['problems']), 'Empty pattern: '+node['id']
if errors: raise SystemExit('\n'.join(errors))
assert (root/'apps/ios/PatternAtlas/Resources/curriculum.json').read_bytes()==(root/'packages/content/curriculum.json').read_bytes()
print(f'Validated {len(nodes)} nodes, all leaf mappings, web/iOS parity, and {checked} Python solution examples.')

assert len(data['problems']) > 2800
assert sum(n['kind']=='collection' and n['id'].startswith('practice-') for n in nodes.values()) == 313
assert len({p['id'] for p in data['problems']})==len(data['problems'])
known={p['id'] for p in data['catalog']}
for node in nodes.values():
    assert set(node.get('problemIds',[])) <= known
for problem in data['problems']:
    assert set(problem.get('collectionIds',[])) <= nodes.keys()
print(f"Validated {sum(p.get('origin')=='community' for p in data['problems'])} attributed community cards (syntax and integrity only).")
