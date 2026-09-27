"""Seeded differential checks for subtle authored algorithms; never runs user drafts."""
import copy
import itertools
import json
import random
from pathlib import Path

rng=random.Random(1947)
data=json.loads((Path(__file__).resolve().parents[1]/'packages/content/curriculum.json').read_text())
implementations={}
for p in data['problems']:
    if p.get('origin') == 'community': continue
    implementations[p['id']]=[]
    for s in p['solutions']:
        scope={}; exec(compile(s['code'],'<authored-solution>','exec'),scope)
        implementations[p['id']].append((s['title'],scope['solve']))
checks=0
def check(number,args,expected):
    global checks
    for title,solve in implementations[str(number)]:
        actual=solve(*copy.deepcopy(args)); assert actual==expected,(number,title,args,actual,expected); checks+=1

for _ in range(100):
    a=[rng.randint(-4,5) for _ in range(rng.randint(1,8))]; k=rng.randint(1,8)
    sums=[sum(a[i:j]) for i in range(len(a)) for j in range(i+1,len(a)+1)]
    check(560,[a,k],sums.count(k))
    check(974,[a,k],sum(s%k==0 for s in sums))
    check(53,[a],max(sums))
    check(862,[a,k],min((j-i for i in range(len(a)) for j in range(i+1,len(a)+1) if sum(a[i:j])>=k),default=-1))
    w=rng.randint(1,len(a)); check(239,[a,w],[max(a[i:i+w]) for i in range(len(a)-w+1)])
    check(907,[a],sum(min(a[i:j]) for i in range(len(a)) for j in range(i+1,len(a)+1))%1_000_000_007)
    s=''.join(rng.choice('abc') for _ in range(rng.randint(1,9)))
    check(899,[s,1],min(s[i:]+s[:i] for i in range(len(s))))
    for title,solve in implementations['1044']:
        result=solve(s)
        best=max((j-i for i in range(len(s)) for j in range(i+1,len(s)+1) if s.find(s[i:j],i+1)>=0),default=0)
        assert len(result)==best and (not result or s.find(result,s.find(result)+1)>=0),(s,title,result,best); checks+=1
    words=list({''.join(rng.choice('abc') for _ in range(rng.randint(1,3))) for _ in range(5)})
    reachable={0}
    for i in range(len(s)):
        if i in reachable:
            for word in words:
                if s.startswith(word,i): reachable.add(i+len(word))
    check(139,[s,words],len(s) in reachable)

for _ in range(50):
    n=rng.randint(1,9); original=[rng.randint(-5,5) for _ in range(n)]; a=original[:]; operations=[]; expected=[]
    for _ in range(20):
        if rng.choice([True,False]):
            i=rng.randrange(n); value=rng.randint(-9,9); operations.append(['update',i,value]); a[i]=value
        else:
            l=rng.randrange(n); r=rng.randrange(l,n); operations.append(['sumRange',l,r]); expected.append(sum(a[l:r+1]))
    check(307,[original,operations],expected)
    bits=[rng.randrange(2) for _ in range(n)]; b=bits[:]; nums2=[rng.randrange(5) for _ in range(n)]; total=sum(nums2); queries=[]; expected=[]
    for _ in range(20):
        kind=rng.randint(1,3)
        if kind==1:
            l=rng.randrange(n); r=rng.randrange(l,n); queries.append([1,l,r])
            for i in range(l,r+1): b[i]^=1
        elif kind==2:
            p=rng.randrange(5); queries.append([2,p,0]); total+=p*sum(b)
        else: queries.append([3,0,0]); expected.append(total)
    check(2569,[bits,nums2,queries],expected)
    graph=[[j for j in range(n) if rng.random()<0.15] for i in range(n)]
    safe=set()
    while True:
        more={i for i,edges in enumerate(graph) if all(v in safe for v in edges)}
        if more<=safe: break
        safe|=more
    check(802,[graph],sorted(safe))

for capacity in range(5):
    values={}; frequency={}; recency={}; operations=[]; expected=[]
    for t in range(100):
        key=rng.randrange(7)
        if rng.random()<0.4:
            operations.append(['get',key]); expected.append(values.get(key,-1))
            if key in values: frequency[key]+=1; recency[key]=t
        else:
            value=rng.randrange(30); operations.append(['put',key,value])
            if not capacity: continue
            if key in values: frequency[key]+=1
            else:
                if len(values)==capacity:
                    victim=min(values,key=lambda x:(frequency[x],recency[x])); del values[victim]; del frequency[victim]; del recency[victim]
                frequency[key]=1
            values[key]=value; recency[key]=t
    check(460,[capacity,operations],expected)
print(f'Passed {checks} seeded differential checks against small brute-force/reference implementations.')
