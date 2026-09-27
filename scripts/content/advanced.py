"""Additional patterns selected by the source coverage audit."""
from .base import category as G, card as C

C('Dynamic programming / Knapsack','Grouped prefix choices',2218,'Advanced','Useful','Choose a prefix from each pile under a total item budget.','For each pile, precompute prefix values and try taking 0..min(pileSize,budget) items from the previous layer.','Reading from the new layer would let one pile be selected more than once.','From each coin pile you may take only a prefix. Choose exactly k coins in total to maximize value.',[[[1,100,3],[7,8,9]],2],101,'''
def solve(piles,k):
    dp=[0]+[float('-inf')]*k
    for pile in piles:
        prefix=[0]
        for x in pile: prefix.append(prefix[-1]+x)
        nxt=dp[:]
        for total in range(1,k+1):
            for take in range(1,min(total,len(pile))+1): nxt[total]=max(nxt[total],dp[total-take]+prefix[take])
        dp=nxt
    return dp[k]
''','O(k × total coins)','O(k + largest pile)')
C('Dynamic programming / Knapsack','Bounded multiplicity counting',2585,'Advanced','Useful','Each choice can be used a limited number of times.','Process one item type per layer and enumerate its allowed count without exceeding the target.','Treat identical questions of one type as indistinguishable choices.','Each type [count,marks] offers count identical questions worth marks each. Count ways to score exactly target, modulo 1,000,000,007.',[6,[[6,1],[3,2],[2,3]]],7,'''
def solve(target,types):
    dp=[1]+[0]*target; mod=1_000_000_007
    for count,marks in types:
        nxt=[0]*(target+1)
        for score in range(target+1):
            nxt[score]=sum(dp[score-used*marks] for used in range(min(count,score//marks)+1))%mod
        dp=nxt
    return dp[target]
''','O(target × sum of multiplicity bounds)','O(target)')
C('Dynamic programming / Compressed & advanced states','Subset partition with remainder',698,'Advanced','Useful','Partition a small set into equal-sum groups.','For each used-item mask, store the filled amount in the current bucket modulo target; completed buckets reset the remainder.','The total sum must divide k, and no item may exceed the bucket target.','Partition positive nums into k nonempty subsets of equal sum if possible.',[[4,3,2,3,5,2,1],4],True,'''
def solve(nums,k):
    total=sum(nums)
    if total%k: return False
    target=total//k
    if max(nums)>target: return False
    dp=[-1]*(1<<len(nums)); dp[0]=0
    for mask in range(len(dp)):
        if dp[mask]<0: continue
        for i,x in enumerate(nums):
            if not mask&(1<<i) and dp[mask]+x<=target: dp[mask|(1<<i)]=(dp[mask]+x)%target
    return dp[-1]==0
''','O(n 2ⁿ)','O(2ⁿ)')
C('Dynamic programming / Compressed & advanced states','Visited-set shortest walk',847,'Advanced','Useful','The future depends on current position and all visited vertices.','Run multi-source BFS over (vertex,visitedMask), starting once at each possible first vertex.','Revisiting a vertex with a different mask is a different state.','In a connected undirected graph, return the fewest edges in a walk visiting every vertex. Vertices and edges may repeat.',[[[1,2,3],[0],[0],[0]]],4,'''
def solve(graph):
    from collections import deque
    n=len(graph); goal=(1<<n)-1; q=deque((i,1<<i,0) for i in range(n)); seen={(i,1<<i) for i in range(n)}
    while q:
        u,mask,d=q.popleft()
        if mask==goal: return d
        for v in graph[u]:
            state=(v,mask|(1<<v))
            if state not in seen: seen.add(state); q.append((*state,d+1))
''','O((V+E) 2ⱽ)','O(V 2ⱽ)')
C('Dynamic programming / Compressed & advanced states','SOS subset aggregation',982,'Advanced','Specialist','Count compatible bitmasks across many subsets.','Count all pairwise AND results, apply a subset-sum transform, then query masks contained in the complement of each third value.','Complement only the relevant bit width, not Python’s unbounded complement.','Count ordered triples of indices i,j,k whose values have bitwise AND zero. Indices may repeat.',[[2,1,3]],12,'''
def solve(nums):
    bits=max(1,max(nums).bit_length()); size=1<<bits; count=[0]*size
    for a in nums:
        for b in nums: count[a&b]+=1
    for bit in range(bits):
        for mask in range(size):
            if mask&(1<<bit): count[mask]+=count[mask^(1<<bit)]
    return sum(count[(size-1)^x] for x in nums)
''','O(n² + B 2ᴮ)','O(2ᴮ)','0 ≤ nums[i] < 2¹⁶.')
C('Dynamic programming / Grids & multiple sequences','Two simultaneous walkers',1463,'Advanced','Useful','Two agents collect values on the same row without double-counting.','Use (row,col1,col2) as state; try the nine pairs of next-column moves, counting a shared cell once.','Separate single-agent optimum paths may overlap and produce a wrong combined answer.','Two robots start in the top-left and top-right cells. Each moves down one row and at most one column sideways. Maximize collected grid values, counting a cell once.',[[[3,1,1],[2,5,1],[1,5,5],[2,1,1]]],24,'''
def solve(grid):
    from functools import cache
    m,n=len(grid),len(grid[0])
    @cache
    def dp(r,a,b):
        if not(0<=a<n and 0<=b<n): return float('-inf')
        reward=grid[r][a]+(grid[r][b] if a!=b else 0)
        if r==m-1: return reward
        return reward+max(dp(r+1,a+x,b+y) for x in (-1,0,1) for y in (-1,0,1))
    return dp(0,0,n-1)
''','O(mn²)','O(mn²)')
C('Dynamic programming / Partitions & intervals','Minimum-cut palindrome partition',132,'Advanced','Useful','Minimize how many valid pieces cover a sequence.','Precompute palindrome intervals while considering endpoints; each palindromic suffix extends an optimal partition of the preceding prefix.','The empty-prefix cut count is −1 so a whole-string palindrome uses zero cuts.','Return the minimum cuts dividing a nonempty string into palindromic substrings.', ['aab'],1,'''
def solve(s):
    n=len(s); palindrome=[[False]*n for _ in range(n)]; cuts=list(range(-1,n))
    for right in range(n):
        for left in range(right+1):
            if s[left]==s[right] and (right-left<2 or palindrome[left+1][right-1]):
                palindrome[left][right]=True; cuts[right+1]=min(cuts[right+1],cuts[left]+1)
    return cuts[n]
''','O(n²)','O(n²)')
C('Dynamic programming / Compressed & advanced states','Digit DP with uniqueness mask',2376,'Advanced','Specialist','Count bounded integers with no repeated digit.','Track position, tightness, and a used-digit mask. A zero mask also represents not having started, so leading zeroes consume no digit.','Exclude the all-leading-zero construction from positive-integer counts.','Count positive integers at most n whose decimal digits are all distinct.',[20],19,'''
def solve(n):
    from functools import cache
    digits=list(map(int,str(n)))
    @cache
    def dp(i,mask,tight):
        if i==len(digits): return int(mask!=0)
        total=0; limit=digits[i] if tight else 9
        for d in range(limit+1):
            nxt=tight and d==limit
            if mask==0 and d==0: total+=dp(i+1,0,nxt)
            elif not mask&(1<<d): total+=dp(i+1,mask|(1<<d),nxt)
        return total
    return dp(0,0,True)
''','O(digits × 2¹⁰ × 10)','O(digits × 2¹⁰)')
C('Dynamic programming / Compressed & advanced states','Prefix-sum transition optimization',629,'Advanced','Specialist','A recurrence sums a sliding interval of previous states.','Insert the largest value into a permutation: it adds 0..size−1 inversions. Maintain a rolling sum over the previous row’s relevant interval.','Subtract the value leaving the transition window before taking modulo.','Count permutations of 1..n with exactly k inverse pairs, modulo 1,000,000,007.',[3,1],2,'''
def solve(n,k):
    mod=1_000_000_007; dp=[1]+[0]*k
    for size in range(1,n+1):
        nxt=[0]*(k+1); window=0
        for inversions in range(k+1):
            window+=dp[inversions]
            if inversions>=size: window-=dp[inversions-size]
            window%=mod; nxt[inversions]=window
        dp=nxt
    return dp[k]
''','O(nk)','O(k)')
C('Dynamic programming / Compressed & advanced states','Matrix exponentiation of transitions',509,'Advanced','Specialist','Apply the same linear transition an enormous number of times.','Represent the recurrence by a fixed matrix and exponentiate it by squaring.','Matrix multiplication order matters even though powers of the same matrix commute.','Return Fibonacci number F(n), with F(0)=0 and F(1)=1.',[10],55,'''
def solve(n):
    def multiply(a,b):
        return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    result=[[1,0],[0,1]]; base=[[1,1],[1,0]]
    while n:
        if n&1: result=multiply(result,base)
        base=multiply(base,base); n//=2
    return result[0][1]
''','O(log n) arithmetic operations','O(1) matrix entries; integers grow with n')
C('Two pointers & windows / Sliding windows','Shortest signed-sum window with deque',862,'Advanced','Useful','Negative values invalidate the usual shrinking-window argument.','Use prefix sums and keep increasing prefix values in a deque. Pop front when the target is reached and pop back when a later prefix dominates an earlier one.','Store the empty prefix at index zero.','Find the shortest nonempty subarray with sum at least k, allowing negative values. Return −1 if absent.',[[2,-1,2],3],3,'''
def solve(nums,k):
    from collections import deque
    q=deque([(0,0)]); prefix=0; best=len(nums)+1
    for i,x in enumerate(nums,1):
        prefix+=x
        while q and prefix-q[0][1]>=k: best=min(best,i-q.popleft()[0])
        while q and q[-1][1]>=prefix: q.pop()
        q.append((i,prefix))
    return best if best<=len(nums) else -1
''','O(n)','O(n)')
C('Two pointers & windows / Sliding windows','Count valid window suffixes',713,'Intermediate','Core','Count all subarrays satisfying a monotone positive-product bound.','After shrinking to a valid window, every suffix ending at right is also valid, contributing right−left+1.','The argument requires positive integers; k≤1 has no answers.','Count nonempty subarrays whose product is strictly less than k. All values are positive integers.',[[10,5,2,6],100],8,'''
def solve(nums,k):
    if k<=1: return 0
    product=1; left=answer=0
    for right,x in enumerate(nums):
        product*=x
        while product>=k: product//=nums[left]; left+=1
        answer+=right-left+1
    return answer
''','O(n)','O(1)')
C('Two pointers & windows / Opposing & forward pointers','Two sorted interval streams',986,'Intermediate','Useful','Intersect two internally disjoint ordered interval lists.','Emit the overlap when max(starts)≤min(ends), then advance whichever interval ends first.','Advance by end time, not by start time.','Return all intersections of two sorted lists of pairwise-disjoint closed intervals.',[[[0,2],[5,10]],[[1,5],[8,12]]],[[1,2],[5,5],[8,10]],'''
def solve(firstList,secondList):
    i=j=0; out=[]
    while i<len(firstList) and j<len(secondList):
        a,b=firstList[i]; c,d=secondList[j]
        if max(a,c)<=min(b,d): out.append([max(a,c),min(b,d)])
        if b<d: i+=1
        else: j+=1
    return out
''','O(m+n)','O(1) excluding output')
C('Arrays & hashing / In-place structure','Grouped run scanning',1446,'Foundation','Useful','Process maximal consecutive runs of equal values.','Move a right pointer to the end of one run, process it once, then begin at that boundary.','Be sure to process the final run.','Return the length of the longest contiguous run consisting of one repeated character.', ['abbcccdddde'],4,'''
def solve(s):
    left=best=0
    while left<len(s):
        right=left+1
        while right<len(s) and s[right]==s[left]: right+=1
        best=max(best,right-left); left=right
    return best
''','O(n)','O(1)')
C('Binary search / Search on the answer','Kth value via cumulative counts',378,'Advanced','Useful','Find the kth smallest value in a row- and column-sorted matrix.','Binary search a value and count how many entries are at most it with a staircase scan.','Duplicates each contribute separately to the rank.','Return the kth smallest value, counting duplicates, in a square matrix sorted by rows and columns.',[[[1,5,9],[10,11,13],[12,13,15]],8],13,'''
def solve(matrix,k):
    n=len(matrix); left,right=matrix[0][0],matrix[-1][-1]
    while left<right:
        mid=(left+right)//2; col=n-1; count=0
        for row in range(n):
            while col>=0 and matrix[row][col]>mid: col-=1
            count+=col+1
        if count>=k: right=mid
        else: left=mid+1
    return left
''','O(n log valueRange)','O(1)')
C('Graphs & grids / Connectivity & structure','Weighted union-find potentials',399,'Advanced','Useful','Maintain multiplicative relations between variables.','Store weight[x]=x/parent[x]. Path compression multiplies weights; merging roots derives a ratio between representatives.','Unknown variables remain unknown even in x/x queries.','Equations a/b=value define positive ratios. Return each queried ratio, or −1.0 when it cannot be established.',[[['a','b'],['b','c']],[2.0,3.0],[['a','c'],['b','a'],['x','x']]],[6.0,0.5,-1.0],'''
def solve(equations,values,queries):
    parent={}; weight={}
    def find(x):
        if parent[x]!=x:
            p=parent[x]; parent[x]=find(p); weight[x]*=weight[p]
        return parent[x]
    for (a,b),value in zip(equations,values):
        for x in (a,b):
            if x not in parent: parent[x]=x; weight[x]=1.0
        ra,rb=find(a),find(b)
        if ra!=rb: parent[ra]=rb; weight[ra]=value*weight[b]/weight[a]
    out=[]
    for a,b in queries:
        if a not in parent or b not in parent or find(a)!=find(b): out.append(-1.0)
        else: out.append(weight[a]/weight[b])
    return out
''','O((E+Q) V) conservative without union by rank','O(V)')
C('Graphs & grids / Connectivity & structure','Kruskal edge selection',1584,'Intermediate','Useful','Build a minimum spanning tree by globally cheapest edges.','Sort all edges and accept an edge only if it joins two different union-find components.','Do not accept edges that close a cycle.','Connect all 2D points with minimum total Manhattan edge cost.',[[[0,0],[2,2],[3,10],[5,2],[7,0]]],20,'''
def solve(points):
    n=len(points); parent=list(range(n)); size=[1]*n
    def find(x):
        while x!=parent[x]: parent[x]=parent[parent[x]]; x=parent[x]
        return x
    edges=sorted((abs(a-c)+abs(b-d),i,j) for i,(a,b) in enumerate(points) for j,(c,d) in enumerate(points) if i<j)
    total=0; chosen=0
    for cost,u,v in edges:
        u,v=find(u),find(v)
        if u==v: continue
        if size[u]<size[v]: u,v=v,u
        parent[v]=u; size[u]+=size[v]; total+=cost; chosen+=1
        if chosen==n-1: break
    return total
''','O(V² log V)','O(V²)')
C('Graphs & grids / Connectivity & structure','Strongly connected component condensation',802,'Advanced','Specialist','Separate directed cycles from the acyclic graph between them.','Use Tarjan’s active-stack low-link algorithm to identify SCCs, mark cyclic SCCs, then propagate unsafety backward through the condensation graph.','An edge to a finished SCC must not lower the current low-link value.','Return sorted vertices from which every directed walk eventually terminates, rather than reaching a cycle.',[[[1,2],[2,3],[5],[0],[5],[],[]]],[2,4,5,6],'''
def solve(graph):
    n=len(graph); index=[-1]*n; low=[0]*n; active=set(); stack=[]; groups=[]; component=[-1]*n; timer=0
    def dfs(u):
        nonlocal timer
        index[u]=low[u]=timer; timer+=1; stack.append(u); active.add(u)
        for v in graph[u]:
            if index[v]<0: dfs(v); low[u]=min(low[u],low[v])
            elif v in active: low[u]=min(low[u],index[v])
        if low[u]==index[u]:
            group=[]
            while True:
                v=stack.pop(); active.remove(v); group.append(v); component[v]=len(groups)
                if v==u: break
            groups.append(group)
    for u in range(n):
        if index[u]<0: dfs(u)
    reverse=[set() for _ in groups]; bad=set()
    for c,group in enumerate(groups):
        if len(group)>1 or any(u in graph[u] for u in group): bad.add(c)
    for u in range(n):
        for v in graph[u]:
            if component[u]!=component[v]: reverse[component[v]].add(component[u])
    todo=list(bad)
    while todo:
        for c in reverse[todo.pop()]:
            if c not in bad: bad.add(c); todo.append(c)
    return [u for u in range(n) if component[u] not in bad]
''','O(V+E)','O(V+E)','Recursive DFS may need an iterative conversion for deep graphs.')
C('Graphs & grids / Connectivity & structure','Bipartite matching by augmenting paths',1820,'Advanced','Specialist','Assign distinct compatible partners to maximize matched pairs.','For each left vertex, search for a free right vertex or reroute its current match. Each successful augment increases matching size by one.','Reset visited right vertices for each augmentation attempt.','grid[i][j]=1 means person i can be paired with partner j. Each person and partner can appear in at most one pair. Return the maximum number of pairs.',[[[1,1,1],[1,0,1],[0,0,1]]],3,'''
def solve(grid):
    m,n=len(grid),len(grid[0]); match=[-1]*n
    def augment(u,seen):
        for v in range(n):
            if grid[u][v] and v not in seen:
                seen.add(v)
                if match[v]<0 or augment(match[v],seen): match[v]=u; return True
        return False
    return sum(augment(u,set()) for u in range(m))
''','O(leftVertices × edges)','O(leftVertices + rightVertices)')
