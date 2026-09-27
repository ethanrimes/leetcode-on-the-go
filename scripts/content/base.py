"""Original curriculum authoring helpers; no runtime network dependency."""
import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
catalog = {p['id']: p for p in json.loads((ROOT / 'packages/content/catalog.json').read_text())['problems']}
nodes = []
problems = {}

def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def category(path, description, approach, tips, topic, level='Intermediate', priority='Core'):
    parts = path.split(' / ')
    key = slug(path)
    nodes.append(dict(id=key, parentId=slug(' / '.join(parts[:-1])) if len(parts)>1 else None,
        title=parts[-1], kind='category', level=level, priority=priority,
        description=description, approach=approach, tips=tips,
        why='Master these building blocks before combining them with other techniques.' if priority=='Core' else 'Learn this family after the core patterns to handle more specialized constraints.',
        sourceUrls=[f'https://leetcode.com/tag/{topic}/']))
    return key

def card(path, title, number, level, priority, cue, insight, pitfall, description, args, expected, code, time, space, constraints='', example_note=''):
    parent = slug(path)
    assert any(n['id']==parent for n in nodes), path
    key = slug(path+' / '+title)
    nodes.append(dict(id=key,parentId=parent,title=title,kind='pattern',level=level,priority=priority,
        description=cue, approach=insight, tips=[pitfall],
        why={'Core':'A reusable foundation: learn the invariant, then recognize it across different stories.', 'Useful':'Adds a new decision rule to your toolkit; study after the foundational patterns.', 'Specialist':'Useful when tighter constraints defeat the standard approach. Learn the prerequisites first.'}[priority],
        sourceUrls=[f'https://leetcode.com/problems/{catalog[str(number)]["slug"]}/']))
    code=textwrap.dedent(code).strip()+'\n'
    signature=next(line for line in code.splitlines() if line.startswith('def solve('))
    solution=dict(patternId=key,title=title,language='Python',approach=insight,code=code,time=time,space=space)
    if str(number) in problems:
        problems[str(number)]['patternIds'].append(key)
        problems[str(number)]['solutions'].append(solution)
    else:
        meta=catalog[str(number)]
        problems[str(number)]=dict(**meta,description=description,examples=[dict(input=json.dumps(args,ensure_ascii=False),output=json.dumps(expected,ensure_ascii=False),note=example_note)],
            constraints=constraints or 'Use the problem-specific input contract described above. See LeetCode for the complete official constraints.',
            patternIds=[key],solutions=[solution],starter=signature+'\n    # State the invariant before you write the loop.\n    pass\n',
            test=dict(args=args,expected=expected),sourceUrl=f'https://leetcode.com/problems/{meta["slug"]}/')
    return key
