"""Compile authoring modules into the same offline artifact for web and SwiftUI."""
import json
import shutil
from pathlib import Path
from content import foundations, dynamic_programming, graphs, trees, structures, search_strings, greedy_math, advanced
from content.base import nodes, problems, ROOT

reference=json.loads((ROOT/'packages/content/reference-index.json').read_text())
families={'Arrays & hashing':'mOr1u6','Two pointers & windows':'0viNMK','Binary search':'SqopEo','Dynamic programming':'tXLS3i','Graphs & grids':'01LUak','Trees & linked lists':'K0n2gO','Stacks, heaps & range queries':'mOr1u6','Backtracking & enumeration':'K0n2gO','Strings & tries':'SJFwQI','Greedy & intervals':'g6KTKL','Sorting & selection':'mOr1u6','Bits, math & geometry':'IYT3ss'}
by_id={n['id']:n for n in nodes}
for node in nodes:
    root=node
    while root['parentId']: root=by_id[root['parentId']]
    guide=next(s for s in reference['sources'] if s['id']==families[root['title']])
    node['sourceUrls'].append(guide['url'])
    direct=[p for p in problems.values() if node['id'] in p['patternIds']]
    matching=[s for s in guide['sections'] if any(p['id'] in s['problemIds'] for p in direct)]
    # These are source-section references, not claims that every linked problem uses this exact leaf pattern.
    node['references']=[dict(title=' / '.join(s['path']),url=guide['url'],problemIds=s['problemIds']) for s in matching]

data=dict(version=1,updatedAt='2026-09-27',language='Python',nodes=nodes,problems=list(problems.values()))
target=ROOT/'packages/content/curriculum.json'
target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
public=ROOT/'apps/web/public/content'; public.mkdir(parents=True,exist_ok=True)
for filename in ('curriculum.json','catalog.json','reference-index.json','official-tags.json'):
    if (ROOT/'packages/content'/filename).exists(): shutil.copyfile(ROOT/'packages/content'/filename,public/filename)
resources=ROOT/'apps/ios/PatternAtlas/Resources'; resources.mkdir(parents=True,exist_ok=True)
shutil.copyfile(target,resources/'curriculum.json')
print(f'Built {sum(n["kind"]=="pattern" for n in nodes)} patterns, {len(problems)} worked problems, {len(nodes)} hierarchy nodes.')
