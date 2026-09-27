"""Import MIT-licensed Python implementations from a pinned local walkccc checkout.

Run: python3 scripts/import_community.py /path/to/walkccc-LeetCode
No upstream source is executed. The committed artifact makes builds reproducible.
"""
import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
checkout = Path(sys.argv[1]).resolve()
commit = subprocess.check_output(['git', '-C', str(checkout), 'rev-parse', 'HEAD'], text=True).strip()
license_text = (checkout / 'LICENSE').read_text()
assert 'MIT License' in license_text and 'Copyright (c) 2022 Peng-Yu Chen' in license_text
catalog = {p['id']: p for p in json.loads((ROOT/'packages/content/catalog.json').read_text())['problems']}
records = []
excluded = []
for directory in sorted((checkout/'solutions').iterdir(), key=lambda p: int(p.name.split('.')[0]) if p.name.split('.')[0].isdigit() else 999999):
    problem_id = directory.name.split('.')[0]
    if problem_id not in catalog: continue
    variants = []
    for path in sorted(directory.glob('*.py'), key=lambda p: (p.stem != problem_id, p.name)):
        code = path.read_text()
        try: ast.parse(code)
        except SyntaxError as error:
            excluded.append(dict(path=str(path.relative_to(checkout)), reason=str(error)))
            continue
        variants.append(dict(code=code, path=str(path.relative_to(checkout)), sha256=hashlib.sha256(code.encode()).hexdigest(), url='https://github.com/walkccc/LeetCode/blob/'+commit+'/'+quote(str(path.relative_to(checkout)))))
    if not variants: continue
    # Keep the public entrypoint signature, without leaking any implementation into the draft.
    tree = ast.parse(variants[0]['code'])
    cls = next((n for n in tree.body if isinstance(n, ast.ClassDef)), None)
    if cls:
        methods = [n for n in cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and (not n.name.startswith('_') or n.name == '__init__')]
        for n in methods: n.body = [ast.Pass()]; n.decorator_list = []
        cls.body = methods or [ast.Pass()]; cls.decorator_list = []
        starter = '# LeetCode-style signature. Read the official statement before drafting.\n'+ast.unparse(ast.Module(body=[cls],type_ignores=[]))+'\n'
    else: starter = '# Write your Python solution here.\n'
    records.append(dict(id=problem_id, starter=starter, solutions=variants))
artifact = dict(repository='https://github.com/walkccc/LeetCode', commit=commit, fetchedAt='2026-09-27', author='Peng-Yu Chen (walkccc)', license='MIT', excluded=excluded, problems=records)
(ROOT/'packages/content/community-solutions.json').write_text(json.dumps(artifact, ensure_ascii=False, indent=2)+'\n')
for directory in ['docs/licenses','apps/web/public/licenses','apps/ios/PatternAtlas/Resources']:
    (ROOT/directory/'walkccc-MIT.txt').write_text(license_text)
print(f'Imported {len(records)} Python problem implementations with {sum(len(p["solutions"]) for p in records)} variants at {commit}.')
