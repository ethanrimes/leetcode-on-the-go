from .base import card as C, problems

C('Stacks, heaps & range queries / Mutable range queries','Lazy segment tree range flips',2569,'Advanced','Specialist','Many range updates affect an aggregate without touching every element.','Store the count of ones per segment and a lazy flip bit. Flipping changes ones to segmentLength−ones; two flips cancel.','Push pending flips before descending into a partially covered segment.','Queries on binary nums1 and integer nums2: [1,l,r] flips nums1 in [l,r]; [2,p,0] adds p*nums1[i] to every nums2[i]; [3,0,0] reports sum(nums2). Return reports.',[[1,0,1],[0,0,0],[[1,1,1],[2,1,0],[3,0,0]]],[3],'''
def solve(nums1,nums2,queries):
    n=len(nums1); tree=[0]*(4*n); lazy=[False]*(4*n)
    def build(v,l,r):
        if l==r: tree[v]=nums1[l]; return
        m=(l+r)//2; build(v*2,l,m); build(v*2+1,m+1,r); tree[v]=tree[v*2]+tree[v*2+1]
    def flip(v,l,r): tree[v]=r-l+1-tree[v]; lazy[v]=not lazy[v]
    def update(v,l,r,a,b):
        if a<=l and r<=b: flip(v,l,r); return
        m=(l+r)//2
        if lazy[v]: flip(v*2,l,m); flip(v*2+1,m+1,r); lazy[v]=False
        if a<=m: update(v*2,l,m,a,b)
        if b>m: update(v*2+1,m+1,r,a,b)
        tree[v]=tree[v*2]+tree[v*2+1]
    build(1,0,n-1); total=sum(nums2); out=[]
    for kind,a,b in queries:
        if kind==1: update(1,0,n-1,a,b)
        elif kind==2: total+=a*tree[1]
        else: out.append(total)
    return out
''','O(n + q log n)','O(n)')
C('Stacks, heaps & range queries / Mutable range queries','Dynamic sparse segment tree',732,'Advanced','Specialist','The coordinate domain is huge but only a few intervals are updated.','Allocate segment nodes only when traversed; store a local lazy increment plus the maximum of child contributions.','Half-open bookings [start,end) become inclusive [start,end−1] for the tree.','After each half-open calendar booking, report the maximum number of simultaneous bookings.',[[[10,20],[50,60],[10,40],[5,15],[5,10],[25,55]]],[1,1,2,3,3,3],'''
def solve(bookings):
    tree={}; lazy={}
    def add(v,l,r,a,b):
        if a<=l and r<=b:
            tree[v]=tree.get(v,0)+1; lazy[v]=lazy.get(v,0)+1; return
        mid=(l+r)//2
        if a<=mid: add(v*2,l,mid,a,b)
        if b>mid: add(v*2+1,mid+1,r,a,b)
        tree[v]=lazy.get(v,0)+max(tree.get(v*2,0),tree.get(v*2+1,0))
    out=[]
    for start,end in bookings: add(1,0,10**9,start,end-1); out.append(tree[1])
    return out
''','O(q log coordinateRange)','O(q log coordinateRange)')
C('Stacks, heaps & range queries / Mutable range queries','Sparse table idempotent queries',239,'Advanced','Specialist','The array is static and many overlapping min/max queries are needed.','Precompute extrema for powers of two. Two possibly overlapping blocks cover each range because max is idempotent.','This overlapping-block trick does not work for sums.','Return the maximum value in every length-k window of an immutable array.',[[1,3,-1,-3,5,3,6,7],3],[3,3,5,5,6,7],'''
def solve(nums,k):
    table=[nums[:]]; width=2
    while width<=len(nums):
        prev=table[-1]; half=width//2
        table.append([max(prev[i],prev[i+half]) for i in range(len(nums)-width+1)])
        width*=2
    power=k.bit_length()-1; block=1<<power
    return [max(table[power][i],table[power][i+k-block]) for i in range(len(nums)-k+1)]
''','O(n log n) preprocessing, O(1) per query','O(n log n)')
C('Stacks, heaps & range queries / Mutable range queries','Square-root decomposition',307,'Intermediate','Useful','Trade simpler implementation for square-root range operations.','Keep raw values plus block sums. Consume boundary elements individually and full interior blocks by summary.','Update the block by the assignment delta.','Simulate point updates and inclusive range-sum queries on nums.',[[1,3,5],[['sumRange',0,2],['update',1,2],['sumRange',0,2]]],[9,8],'''
def solve(nums,operations):
    from math import isqrt
    n=len(nums); width=isqrt(n)+1; a=nums[:]; blocks=[0]*((n+width-1)//width)
    for i,x in enumerate(a): blocks[i//width]+=x
    out=[]
    for kind,l,r in operations:
        if kind=='update': blocks[l//width]+=r-a[l]; a[l]=r; continue
        total=0
        while l<=r and l%width: total+=a[l]; l+=1
        while l+width-1<=r: total+=blocks[l//width]; l+=width
        while l<=r: total+=a[l]; l+=1
        out.append(total)
    return out
''','O(n + q√n), O(1) per update','O(n)')
C('Graphs & grids / Connectivity & structure','Offline sorted-threshold connectivity',1697,'Advanced','Useful','Many connectivity queries permit edges only below a changing threshold.','Sort edges and queries by limit. Incrementally union newly permitted edges, answering queries in that order and restoring output order.','The threshold is strict: an edge equal to limit is excluded.','For each query [p,q,limit], report whether p and q connect using only edges whose weights are below limit.',[3,[[0,1,2],[1,2,4],[2,0,8]],[[0,1,2],[0,2,5]]],[False,True],'''
def solve(n,edgeList,queries):
    parent=list(range(n)); size=[1]*n
    def find(x):
        while x!=parent[x]: parent[x]=parent[parent[x]]; x=parent[x]
        return x
    edges=sorted(edgeList,key=lambda e:e[2]); cursor=0; out=[False]*len(queries)
    for i,(a,b,limit) in sorted(enumerate(queries),key=lambda q:q[1][2]):
        while cursor<len(edges) and edges[cursor][2]<limit:
            u,v,_=edges[cursor]; u,v=find(u),find(v)
            if u!=v:
                if size[u]<size[v]: u,v=v,u
                parent[v]=u; size[u]+=size[v]
            cursor+=1
        out[i]=find(a)==find(b)
    return out
''','O(E log E + Q log Q + (E+Q) α(V))','O(V+E+Q)')
C('Strings & tries / Matching & palindrome structure','Suffix array and adjacent LCP',1044,'Advanced','Specialist','Find the longest repeated substring, allowing overlaps.','Sort suffixes by doubling ranked prefixes. The largest common prefix of adjacent suffixes is the longest repeat; compute LCPs using Kasai’s reuse invariant.','Avoid constructing all suffix strings, which uses quadratic space.','Return a longest substring appearing at least twice in s. Occurrences may overlap; return empty when none repeats.', ['banana'],'ana','''
def solve(s):
    n=len(s); sa=list(range(n)); rank=list(map(ord,s)); k=1
    while k<n:
        key=lambda i:(rank[i],rank[i+k] if i+k<n else -1)
        sa.sort(key=key); new=[0]*n
        for j in range(1,n): new[sa[j]]=new[sa[j-1]]+(key(sa[j-1])!=key(sa[j]))
        rank=new
        if rank[sa[-1]]==n-1: break
        k*=2
    position=[0]*n
    for i,start in enumerate(sa): position[start]=i
    length=best=start=0
    for i in range(n):
        r=position[i]
        if r==0: length=0; continue
        j=sa[r-1]
        while i+length<n and j+length<n and s[i+length]==s[j+length]: length+=1
        if length>best: best,start=length,i
        length=max(0,length-1)
    return s[start:start+best]
''','O(n log² n)','O(n)')
C('Strings & tries / Prefix indexes','Aho–Corasick multi-pattern matching',139,'Advanced','Specialist','Many dictionary words must be matched during one text scan.','Build trie failure links to the longest suffix that is also a trie prefix. Each terminal match offers a word-break DP transition.','Failure links must carry terminal outputs from suffix states.','Determine whether a string can be segmented into dictionary words, which may be reused.', ['applepenapple',['apple','pen']],True,'''
def solve(s,wordDict):
    from collections import deque
    children=[{}]; fail=[0]; output=[[]]
    for word in wordDict:
        node=0
        for ch in word:
            if ch not in children[node]: children[node][ch]=len(children); children.append({}); fail.append(0); output.append([])
            node=children[node][ch]
        output[node].append(len(word))
    q=deque(children[0].values())
    while q:
        u=q.popleft()
        for ch,v in children[u].items():
            f=fail[u]
            while f and ch not in children[f]: f=fail[f]
            fail[v]=children[f].get(ch,0); output[v]+=output[fail[v]]; q.append(v)
    dp=[True]+[False]*len(s); node=0
    for i,ch in enumerate(s,1):
        while node and ch not in children[node]: node=fail[node]
        node=children[node].get(ch,0)
        dp[i]=any(dp[i-length] for length in output[node])
    return dp[-1]
''','O(trie construction including failure/output expansion + text + matches)','O(trie nodes + inherited outputs + text)')
C('Strings & tries / Matching & palindrome structure','Minimal cyclic rotation',899,'Advanced','Specialist','Choose the lexicographically smallest rotation.','For k=1 only rotations are reachable: compare two candidate starts and skip dominated starts after a mismatch. With k>1, arbitrary sorting is reachable.','A mismatch eliminates an entire range of starts, making the rotation scan linear.','Repeatedly move one of the first k characters of s to its end. Return the lexicographically smallest reachable string.', ['cba',1],'acb','''
def solve(s,k):
    if k>1: return ''.join(sorted(s))
    n=len(s); doubled=s+s; i,j,offset=0,1,0
    while i<n and j<n and offset<n:
        a,b=doubled[i+offset],doubled[j+offset]
        if a==b: offset+=1; continue
        if a>b:
            i+=offset+1
            if i==j: i+=1
        else:
            j+=offset+1
            if i==j: j+=1
        offset=0
    start=min(i,j)
    return doubled[start:start+n]
''','O(n) for k=1; O(n log n) otherwise','O(n)')
C('Bits, math & geometry / Geometry & randomness','Convex hull with cross products',587,'Advanced','Specialist','Find the boundary of a point set.','Build lower and upper monotone chains, popping turns that bend inward. Keep collinear boundary points by popping only strictly wrong turns.','The strictness differs when only extreme hull vertices are wanted.','Return every tree point lying on the boundary of the smallest enclosing fence, including collinear boundary points. Order is irrelevant.',[[[1,1],[2,2],[2,0],[2,4],[3,3],[4,2]]],[[1,1],[2,0],[2,4],[3,3],[4,2]],'''
def solve(trees):
    points=sorted(map(tuple,trees))
    def cross(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def half(seq):
        out=[]
        for p in seq:
            while len(out)>=2 and cross(out[-2],out[-1],p)<0: out.pop()
            out.append(p)
        return out
    return [list(p) for p in sorted(set(half(points)+half(points[::-1])))]
''','O(n log n)','O(n)')
C('Bits, math & geometry / Number theory & counting','Inclusion–exclusion with LCM',1201,'Advanced','Useful','Count numbers divisible by at least one of several factors.','Add single-factor counts, subtract pair intersections, and add the triple intersection. Binary search the first value whose union count reaches n.','Intersections use LCM, not the product when factors overlap.','Return the nth positive integer divisible by at least one of a, b, or c.',[3,2,3,5],4,'''
def solve(n,a,b,c):
    from math import lcm
    ab,ac,bc,abc=lcm(a,b),lcm(a,c),lcm(b,c),lcm(a,b,c)
    left,right=1,n*min(a,b,c)
    while left<right:
        x=(left+right)//2
        count=x//a+x//b+x//c-x//ab-x//ac-x//bc+x//abc
        if count>=n: right=x
        else: left=x+1
    return left
''','O(log(n × min(a,b,c))) arithmetic operations','O(1)')
C('Bits, math & geometry / Geometry & randomness','Rejection sampling without modulo bias',470,'Intermediate','Useful','Create a uniform target range from a different uniform source.','Two independent rand7 calls create 49 equally likely outcomes. Accept the first 40 and map them into ten equal buckets.','Taking modulo ten across all 49 outcomes is biased.','Implement rand10 using a uniform rand7 source. This standalone study version simulates rand7 with random.randint; on LeetCode use the supplied rand7.',[],1,'''
def solve():
    import random
    def rand7(): return random.randint(1,7)
    while True:
        value=(rand7()-1)*7+rand7()-1
        if value<40: return value%10+1
''','O(1) expected; unbounded worst-case retries','O(1)',example_note='A random integer from 1 through 10; 1 is one possible outcome.')
problems['470']['test']['comparison']='rand10'
C('Bits, math & geometry / Geometry & randomness','Fisher–Yates shuffle',384,'Intermediate','Useful','Generate each permutation with equal probability.','At position i from the end, swap with a uniformly chosen position in [0,i]. Fix that position permanently.','Sampling from the full array at every step produces a biased shuffle.','Return a uniformly shuffled copy of nums. A reset operation would return the preserved original array.',[[1,2,3]],[1,2,3],'''
def solve(nums):
    import random
    out=nums[:]
    for i in range(len(out)-1,0,-1):
        j=random.randrange(i+1); out[i],out[j]=out[j],out[i]
    return out
''','O(n)','O(n)',example_note='Any permutation is valid; the sample shows one possible outcome.')
problems['384']['test']['comparison']='permutation'
C('Stacks, heaps & range queries / Data structure design','Random access with swap-delete',380,'Intermediate','Core','Support insert, remove, and random selection in expected constant time.','Combine an array with value-to-index lookup. Delete by moving the last value into the removed slot and repairing its index.','Update the swapped value’s position before removing the key.','Simulate insert/remove/getRandom. Insert and remove return success booleans; getRandom chooses uniformly from current values and is never called on an empty set.',[[['insert',1],['insert',2],['remove',1],['getRandom']]],[True,True,True,2],'''
def solve(operations):
    import random
    values=[]; index={}; out=[]
    for op in operations:
        if op[0]=='getRandom': out.append(random.choice(values)); continue
        x=op[1]
        if op[0]=='insert':
            if x in index: out.append(False)
            else: index[x]=len(values); values.append(x); out.append(True)
        else:
            if x not in index: out.append(False)
            else:
                i=index[x]; last=values[-1]; values[i]=last; index[last]=i
                values.pop(); del index[x]; out.append(True)
    return out
''','O(1) expected per operation','O(number of stored values)')
C('Stacks, heaps & range queries / Data structure design','LFU frequency buckets',460,'Advanced','Useful','Evict by access frequency, breaking ties by recency.','Keep an ordered bucket for each frequency and track the minimum active frequency. Access moves an item to the next frequency bucket.','Updating an existing value counts as an access; new items start at frequency one.','Simulate LFU cache put/get operations. When full, evict the least-frequent key, preferring the least recently used among ties. Return get results.',[2,[['put',1,1],['put',2,2],['get',1],['put',3,3],['get',2],['get',3]]],[1,-1,3],'''
def solve(capacity,operations):
    from collections import defaultdict,OrderedDict
    values={}; frequency={}; buckets=defaultdict(OrderedDict); minimum=0; out=[]
    def touch(key):
        nonlocal minimum
        f=frequency[key]; del buckets[f][key]
        if not buckets[f]:
            del buckets[f]
            if f==minimum: minimum+=1
        frequency[key]=f+1; buckets[f+1][key]=None
    for op in operations:
        key=op[1]
        if op[0]=='get':
            out.append(values.get(key,-1))
            if key in values: touch(key)
        elif capacity:
            if key in values: values[key]=op[2]; touch(key); continue
            if len(values)==capacity:
                old,_=buckets[minimum].popitem(last=False); del values[old]; del frequency[old]
                if not buckets[minimum]: del buckets[minimum]
            values[key]=op[2]; frequency[key]=1; buckets[1][key]=None; minimum=1
    return out
''','O(1) expected per operation','O(capacity)')
C('Stacks, heaps & range queries / Data structure design','Lazy nested iterator',341,'Intermediate','Useful','Flatten nested values without eagerly expanding the whole structure.','Keep a stack of iterators. Advance the top iterator; push a child iterator for a nested list and pop exhausted iterators.','hasNext implementations must not consume a value unless they cache it for next.','Flatten an arbitrarily nested list of integers in left-to-right order. This study wrapper collects the outputs of a lazy generator.',[[[1,1],2,[1,[3]]]], [1,1,2,1,3],'''
def solve(nestedList):
    def flattened():
        stack=[iter(nestedList)]
        while stack:
            try: value=next(stack[-1])
            except StopIteration: stack.pop(); continue
            if isinstance(value,int): yield value
            else: stack.append(iter(value))
    return list(flattened())
''','O(total nested entries)','O(nesting depth) auxiliary, excluding output')
C('Stacks, heaps & range queries / Data structure design','Circular buffer queue',622,'Foundation','Useful','Reuse a fixed capacity array for FIFO operations.','Track a head index and count; the insertion position is (head+count) modulo capacity.','Distinguish full and empty with a count rather than ambiguous equal pointers.','Simulate enQueue(value), deQueue, Front, Rear, isEmpty, and isFull for a fixed-size circular queue. Return each operation result.',[2,[['enQueue',1],['enQueue',2],['enQueue',3],['Rear'],['deQueue'],['Front']]],[True,True,False,2,True,2],'''
def solve(k,operations):
    values=[0]*k; head=count=0; out=[]
    for op in operations:
        kind=op[0]
        if kind=='enQueue':
            out.append(count<k)
            if count<k: values[(head+count)%k]=op[1]; count+=1
        elif kind=='deQueue':
            out.append(count>0)
            if count: head=(head+1)%k; count-=1
        elif kind=='Front': out.append(values[head] if count else -1)
        elif kind=='Rear': out.append(values[(head+count-1)%k] if count else -1)
        elif kind=='isEmpty': out.append(count==0)
        else: out.append(count==k)
    return out
''','O(1) per operation','O(k)','Capacity k is positive.')
C('Trees & linked lists / Tree dynamic programming','Binary lifting ancestor queries',1483,'Advanced','Useful','Answer large ancestor jumps repeatedly on a fixed tree.','Precompute each node’s 2^b-th ancestor by composing two 2^(b−1) jumps. Decompose k into binary bits.','Stop if an ancestor is absent or a requested bit exceeds the table.','Given a parent array with root parent −1 and queries [node,k], return each node’s kth ancestor, or −1.',[[-1,0,0,1,1,2,2],[[3,1],[5,2],[6,3]]],[1,0,-1],'''
def solve(parent,queries):
    n=len(parent); levels=max(1,n.bit_length()); up=[parent[:]]
    for b in range(1,levels): up.append([up[b-1][up[b-1][v]] if up[b-1][v]>=0 else -1 for v in range(n)])
    out=[]
    for node,k in queries:
        bit=0
        while k and node!=-1:
            if bit>=levels: node=-1; break
            if k&1: node=up[bit][node]
            k>>=1; bit+=1
        out.append(node)
    return out
''','O(n log n + q log k)','O(n log n)')
C('Bits, math & geometry / Number theory & counting','Losing-state modular invariant',292,'Foundation','Useful','A small impartial game repeats after a fixed move range.','Positions divisible by four are losing when players may remove one to three stones. From any other position move to a multiple of four.','Explain the inductive losing-state argument, not just the modulo trick.','Two optimal players remove 1, 2, or 3 stones per turn from a pile of n. The player taking the last stone wins. Does the first player win?', [8],False,'''
def solve(n):
    return n%4!=0
''','O(1)','O(1)')
C('Bits, math & geometry / Number theory & counting','Multiplicative combinatorial counting',62,'Foundation','Core','A path is an ordering of a fixed number of two move types.','Choose which positions contain down moves among all moves. The answer is a binomial coefficient.','Count move positions, not grid cells; there are m+n−2 moves.','Count paths from top-left to bottom-right of an m×n grid using only down and right moves.',[3,7],28,'''
def solve(m,n):
    from math import comb
    return comb(m+n-2,m-1)
''','O(min(m,n)) multiplicative steps conceptually; big-integer costs apply','O(1) integer objects')
C('Binary search / Ordered positions','Interactive monotone oracle',374,'Foundation','Useful','An API tells whether a guess is too low or too high.','Binary search the hidden value using only the oracle response; preserve a closed interval of possible answers.','The oracle compares your guess to the hidden number, so check its sign convention.','Find a hidden integer in 1..n. The platform oracle returns −1 for a guess too high, +1 for too low, and 0 for correct. Study input includes the hidden value to simulate the oracle.',[10,6],6,'''
def solve(n,hidden):
    def guess(value): return (hidden>value)-(hidden<value)
    left,right=1,n
    while left<=right:
        mid=(left+right)//2; response=guess(mid)
        if response==0: return mid
        if response>0: left=mid+1
        else: right=mid-1
''','O(log n) oracle calls','O(1)')
