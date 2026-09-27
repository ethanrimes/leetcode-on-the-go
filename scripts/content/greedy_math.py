from .base import category as G, card as C

G('Greedy & intervals','Make a local choice only when an exchange argument or invariant proves it safe.','Find a way to transform an optimal answer to include your choice without worsening it.',['Sorting is often the step that makes a greedy decision valid.','Try a small counterexample before trusting intuition.'],'greedy')
G('Greedy & intervals / Interval decisions','Order intervals by the boundary relevant to your objective.','Use start order for merging, end order for maximum compatible selections, and events for overlap counts.',['Decide whether touching endpoints overlap.'],'greedy')
C('Greedy & intervals / Interval decisions','Merge overlapping intervals',56,'Intermediate','Core','Combine ranges into disjoint coverage.','Sort by starting position. Extend the previous range if it overlaps; otherwise start a new range.','Closed intervals sharing an endpoint overlap here.','Merge overlapping closed intervals and return them in increasing start order.',[[[1,3],[2,6],[8,10]]],[[1,6],[8,10]],'''
def solve(intervals):
    out=[]
    for start,end in sorted(intervals):
        if out and start<=out[-1][1]: out[-1][1]=max(out[-1][1],end)
        else: out.append([start,end])
    return out
''','O(n log n)','O(n)')
C('Greedy & intervals / Interval decisions','Earliest-finish scheduling',435,'Intermediate','Core','Keep as many nonoverlapping intervals as possible.','Sort by end time and keep each interval that starts at or after the previous chosen end. Earlier finishes leave at least as much room.','For this scheduling problem, touching endpoints are compatible.','Return the fewest intervals to remove so remaining intervals do not overlap.',[[[1,2],[2,3],[3,4],[1,3]]],1,'''
def solve(intervals):
    end=float('-inf'); kept=0
    for a,b in sorted(intervals,key=lambda x:x[1]):
        if a>=end: kept+=1; end=b
    return len(intervals)-kept
''','O(n log n)','O(n)')
C('Greedy & intervals / Interval decisions','Sweep-line overlap count',2406,'Intermediate','Useful','Allocate the minimum groups so no group contains overlapping intervals.','Convert closed intervals to +1 at start and −1 at end+1; the maximum active count is the required number of groups.','A closed interval still overlaps another beginning at its endpoint.','Partition closed integer intervals into the fewest groups such that intervals in one group never overlap.',[[[1,3],[2,4],[5,6]]],2,'''
def solve(intervals):
    events={}
    for a,b in intervals: events[a]=events.get(a,0)+1; events[b+1]=events.get(b+1,0)-1
    active=best=0
    for t in sorted(events): active+=events[t]; best=max(best,active)
    return best
''','O(n log n)','O(n)')
G('Greedy & intervals / Reachability & exchange','Maintain the strongest feasible prefix or replace a previous decision.','Summarize all choices so far with a frontier, balance, or heap of replaceable commitments.',['A replacement may be more important than making the next choice.'],'greedy')
C('Greedy & intervals / Reachability & exchange','Farthest reachable frontier',55,'Intermediate','Core','Each position extends a reachable prefix.','Scan only reachable positions and extend the farthest reachable index.','If the scan passes the frontier, no later value can rescue the gap.','Each nonnegative nums[i] is the maximum forward jump length. Determine whether the last index is reachable from index 0.',[[2,3,1,1,4]],True,'''
def solve(nums):
    farthest=0
    for i,x in enumerate(nums):
        if i>farthest: return False
        farthest=max(farthest,i+x)
    return True
''','O(n)','O(1)')
C('Greedy & intervals / Reachability & exchange','Jump layers as implicit BFS',45,'Intermediate','Core','Find the minimum jumps when all reachable next positions form an interval.','Track the end of the current jump layer and the farthest point the next layer can reach. Commit a jump at the current boundary.','Do not count a jump after processing the last index.','Given a reachable nonnegative jump array, return the fewest jumps from first to last index.',[[2,3,1,1,4]],2,'''
def solve(nums):
    end=farthest=jumps=0
    for i in range(len(nums)-1):
        farthest=max(farthest,i+nums[i])
        if i==end: jumps+=1; end=farthest
    return jumps
''','O(n)','O(1)')
C('Greedy & intervals / Reachability & exchange','Reset after negative balance',134,'Intermediate','Useful','A circular traversal accumulates gains and costs.','If a segment balance turns negative, no start within that failed segment can succeed before its end; restart after it.','The total balance must be nonnegative for any solution.','At station i collect gas[i] and spend cost[i] to reach the next station. Return a valid start for a full loop, or −1.',[[1,2,3,4,5],[3,4,5,1,2]],3,'''
def solve(gas,cost):
    total=tank=start=0
    for i,(g,c) in enumerate(zip(gas,cost)):
        total+=g-c; tank+=g-c
        if tank<0: start=i+1; tank=0
    return start if total>=0 else -1
''','O(n)','O(1)')
C('Greedy & intervals / Reachability & exchange','Regret heap scheduling',630,'Advanced','Useful','Keep the most tasks under completion deadlines.','Sort by deadline, tentatively add each duration, and remove the longest chosen duration whenever the total exceeds the current deadline.','Discard the longest selected task, which may be a previous one.','Courses are [duration,lastDay]. Starting at day 1 and taking one course at a time, maximize the number finished by their deadlines.',[[[100,200],[200,1300],[1000,1250],[2000,3200]]],3,'''
def solve(courses):
    from heapq import heappush,heappop
    heap=[]; elapsed=0
    for duration,deadline in sorted(courses,key=lambda x:x[1]):
        elapsed+=duration; heappush(heap,-duration)
        if elapsed>deadline: elapsed+=heappop(heap)
    return len(heap)
''','O(n log n)','O(n)')
C('Greedy & intervals / Reachability & exchange','Partition by last occurrence',763,'Intermediate','Useful','Split a sequence so each symbol appears in one part only.','Extend the current endpoint to every encountered symbol’s last position. Close a part when the scan reaches that endpoint.','A symbol inside the current part can push the endpoint farther.','Partition a string into as many parts as possible so each letter appears in at most one part. Return part lengths.', ['ababcbacadefegdehijhklij'],[9,7,8],'''
def solve(s):
    last={ch:i for i,ch in enumerate(s)}; start=end=0; out=[]
    for i,ch in enumerate(s):
        end=max(end,last[ch])
        if i==end: out.append(i-start+1); start=i+1
    return out
''','O(n)','O(alphabet size) excluding output')

G('Sorting & selection','Create order or isolate ranks without doing unnecessary work.','Choose comparison sorting, bounded-domain counting, or partition-based selection according to constraints.',['Sorting may change index meaning; preserve original indices when needed.'],'sorting')
C('Sorting & selection','Merge-sort divide and conquer',912,'Foundation','Core','Sort by solving independent halves and combining ordered outputs.','Recursively sort two halves, then merge using two read pointers.','Selecting the left value on equal keys preserves stability.','Return the integers in ascending order.',[[5,2,3,1]],[1,2,3,5],'''
def solve(nums):
    if len(nums)<2: return nums[:]
    mid=len(nums)//2; left=solve(nums[:mid]); right=solve(nums[mid:]); out=[]; i=j=0
    while i<len(left) and j<len(right):
        if left[i]<=right[j]: out.append(left[i]); i+=1
        else: out.append(right[j]); j+=1
    return out+left[i:]+right[j:]
''','O(n log n)','O(n) live auxiliary space')
C('Sorting & selection','Randomized quickselect',215,'Intermediate','Useful','Find one rank without sorting everything.','Partition around a randomly selected pivot into smaller, equal, and larger values, then recurse only into the side containing the target rank.','Three-way partitioning avoids pathological behavior on duplicate values.','Return the kth largest array value, including duplicates.',[[3,2,1,5,6,4],2],5,'''
def solve(nums,k):
    import random
    a=nums[:]; index=len(a)-k
    while True:
        pivot=random.choice(a); low=[x for x in a if x<pivot]; same=sum(x==pivot for x in a)
        if index<len(low): a=low
        elif index<len(low)+same: return pivot
        else: index-=len(low)+same; a=[x for x in a if x>pivot]
''','O(n) expected; O(n²) worst','O(n)')
C('Sorting & selection','Frequency buckets',347,'Intermediate','Core','Rank items by an integer frequency bounded by input size.','Count values, bucket them by frequency, and scan buckets from largest to smallest.','Frequency is the bucket index, not the original value.','Return the k most frequent integers; the set of top-k values is guaranteed unique. Order is irrelevant.',[[1,1,1,2,2,3],2],[1,2],'''
def solve(nums,k):
    from collections import Counter
    buckets=[[] for _ in range(len(nums)+1)]
    for x,count in Counter(nums).items(): buckets[count].append(x)
    out=[]
    for bucket in reversed(buckets):
        out.extend(bucket)
        if len(out)>=k: return out[:k]
''','O(n)','O(n)')
C('Sorting & selection','Radix sorting fixed-width digits',164,'Advanced','Specialist','Sort nonnegative integers by digits to avoid comparison bounds.','Perform stable counting passes from least significant to most significant digit, then inspect adjacent gaps.','Every pass must be stable to preserve the previous digit order.','Return the largest difference between adjacent values after sorting nonnegative nums; return 0 for fewer than two values.',[[3,6,9,1]],3,'''
def solve(nums):
    if len(nums)<2: return 0
    a=nums[:]; place=1; maximum=max(a)
    while maximum//place:
        buckets=[[] for _ in range(10)]
        for x in a: buckets[(x//place)%10].append(x)
        a=[x for bucket in buckets for x in bucket]; place*=10
    return max(b-a for a,b in zip(a,a[1:]))
''','O(n × number of digits)','O(n)')

G('Bits, math & geometry','Exploit representation, arithmetic structure, and geometric invariants.','Translate operations into algebra before selecting an implementation.',['Watch overflow in fixed-width languages.','State the random distribution or numeric precision assumptions.'],'math')
G('Bits, math & geometry / Bit representations','Treat an integer as a compact set of boolean choices.','Use XOR for parity, AND for intersection, and shifts to address individual bits.',['Python integers are unbounded; negative bit behavior differs from fixed-width words.'],'bit-manipulation')
C('Bits, math & geometry / Bit representations','XOR cancellation',136,'Foundation','Core','All values occur twice except one.','Equal values cancel under XOR and zero is the identity, leaving the odd-occurrence value.','This rule depends on the exact multiplicity guarantee.','Return the one value occurring once when every other value occurs exactly twice.',[[4,1,2,1,2]],4,'''
def solve(nums):
    result=0
    for x in nums: result^=x
    return result
''','O(n)','O(1)')
C('Bits, math & geometry / Bit representations','Remove the lowest set bit',191,'Foundation','Core','Count set bits without scanning zero bits.','n & (n−1) removes the least significant set bit; repeat until the number becomes zero.','This loop assumes a nonnegative fixed-width input.','Return the number of 1 bits in a nonnegative 32-bit integer.',[11],3,'''
def solve(n):
    count=0
    while n: n &= n-1; count+=1
    return count
''','O(number of set bits)','O(1)')
C('Bits, math & geometry / Bit representations','Common binary prefix',201,'Intermediate','Useful','AND every number in a contiguous integer range.','Shift both boundaries until they match; all lower differing bits vanish somewhere in the range.','Do not iterate through the entire numeric range.','Return the bitwise AND of all integers in inclusive [left,right], with nonnegative bounds.',[5,7],4,'''
def solve(left,right):
    shift=0
    while left!=right: left>>=1; right>>=1; shift+=1
    return left<<shift
''','O(log right)','O(1)')
C('Bits, math & geometry / Bit representations','Distinct suffix-OR compression',898,'Advanced','Useful','All suffix ORs change only when a new bit appears.','Maintain the distinct OR values of subarrays ending here; OR each previous value with x and include x itself.','The number of distinct states is bounded by bit width, not array length.','Return how many distinct bitwise-OR results are produced by nonempty subarrays.',[[1,2,4]],6,'''
def solve(arr):
    ending=set(); all_values=set()
    for x in arr:
        ending={x}|{value|x for value in ending}; all_values.update(ending)
    return len(all_values)
''','O(n log U)','O(n log U)')
G('Bits, math & geometry / Number theory & counting','Use divisibility and combinatorial structure to shrink the search.','Reduce by gcd, factor repeated contributions, or count equivalent outcomes instead of enumerating them.',['Use modular arithmetic throughout large counting recurrences.'],'number-theory')
C('Bits, math & geometry / Number theory & counting','Euclidean gcd structure',1071,'Foundation','Useful','A common repeating block must divide both lengths.','If concatenating in either order gives the same string, the gcd-length prefix is the largest common block.','Compatible lengths alone do not prove compatible content.','Return the longest string that can repeat to form both input strings, or empty if no such string exists.', ['ABCABC','ABC'],'ABC','''
def solve(str1,str2):
    from math import gcd
    return str1[:gcd(len(str1),len(str2))] if str1+str2==str2+str1 else ''
''','O(m+n)','O(m+n)')
C('Bits, math & geometry / Number theory & counting','Sieve of Eratosthenes',204,'Intermediate','Core','Find many primes below a bound.','Mark multiples of each prime starting at its square; smaller multiples already have a smaller prime factor.','The problem asks for primes strictly below n.','Count primes p satisfying 0≤p<n.',[20],8,'''
def solve(n):
    if n<2: return 0
    prime=[True]*n; prime[0]=prime[1]=False; p=2
    while p*p<n:
        if prime[p]:
            for multiple in range(p*p,n,p): prime[multiple]=False
        p+=1
    return sum(prime)
''','O(n log log n)','O(n)')
C('Bits, math & geometry / Number theory & counting','Exponentiation by squaring',50,'Intermediate','Core','Compute a large power with logarithmically many multiplications.','Square the base each step and multiply it into the result when the current exponent bit is set.','Invert the base once for negative exponents.','Return x raised to integer power n. For negative n, x is nonzero.',[2.0,-3],0.125,'''
def solve(x,n):
    if n<0: x=1/x; n=-n
    answer=1.0
    while n:
        if n&1: answer*=x
        x*=x; n>>=1
    return answer
''','O(log |n|)','O(1)')
C('Bits, math & geometry / Number theory & counting','Prime valuation in factorials',172,'Foundation','Useful','Count trailing zeroes without computing a factorial.','Each zero needs factors 2 and 5; twos are abundant, so count multiples of 5, 25, 125, and so on.','Multiples of 25 contribute more than one factor of five.','Return the number of trailing decimal zeroes in n factorial.',[25],6,'''
def solve(n):
    answer=0
    while n: n//=5; answer+=n
    return answer
''','O(log₅ n)','O(1)')
C('Bits, math & geometry / Number theory & counting','Catalan decomposition',96,'Intermediate','Useful','A root independently splits ordered keys into left and right substructures.','Sum leftCount × rightCount across each possible root split.','An empty subtree has one possible structure.','Return the number of structurally distinct BSTs containing values 1..n.',[3],5,'''
def solve(n):
    dp=[1]+[0]*n
    for size in range(1,n+1):
        dp[size]=sum(dp[left]*dp[size-1-left] for left in range(size))
    return dp[n]
''','O(n²)','O(n)')
G('Bits, math & geometry / Geometry & randomness','Use exact invariants for geometry and explicit distributions for sampling.','Prefer integer cross products for orientation and cumulative counts for weighted random choices.',['Avoid floating-point slopes for collinearity.'],'geometry','Advanced','Useful')
C('Bits, math & geometry / Geometry & randomness','Normalized slope counting',149,'Advanced','Useful','Find the largest collinear set.','Fix an anchor and group other points by reduced (dx,dy), using gcd and a consistent sign convention.','Vertical and horizontal lines need the same normalization discipline.','Return the largest number of distinct 2D integer points lying on one straight line.',[[[1,1],[2,2],[3,3],[3,1]]],3,'''
def solve(points):
    from math import gcd
    best=1
    for i,(x,y) in enumerate(points):
        counts={}
        for a,b in points[i+1:]:
            dx,dy=a-x,b-y; g=gcd(dx,dy); dx//=g; dy//=g
            if dx<0 or (dx==0 and dy<0): dx,dy=-dx,-dy
            counts[dx,dy]=counts.get((dx,dy),0)+1; best=max(best,counts[dx,dy]+1)
    return best
''','O(n² log coordinateRange)','O(n)','Points are distinct; at least one point.')
C('Bits, math & geometry / Geometry & randomness','Reservoir sampling',398,'Intermediate','Useful','Uniformly select one matching position from an unknown-length stream.','On the kth matching occurrence, replace the selected index with probability 1/k. Each prior choice survives with the complementary probability.','Choosing the first match or sampling values instead of indices is biased.','Return a uniformly random index containing target. A target occurrence is guaranteed. Example output shows one possible result.',[[4,8,4],8],1,'''
def solve(nums,target):
    import random
    count=0; chosen=-1
    for i,x in enumerate(nums):
        if x==target:
            count+=1
            if random.randrange(count)==0: chosen=i
    return chosen
''','O(n) per pick','O(1)')
C('Bits, math & geometry / Geometry & randomness','Weighted prefix sampling',528,'Intermediate','Useful','Select an index with probability proportional to a positive weight.','Build cumulative weights, draw an integer from 1 through total, then find the first cumulative weight at least that integer.','Use inclusive integer bounds consistently to avoid off-by-one bias.','Given positive weights, pick one index with probability weight[i]/sum(weights). Example output is deterministic because there is one weight.',[[7]],0,'''
def solve(weights):
    from itertools import accumulate
    from bisect import bisect_left
    import random
    prefix=list(accumulate(weights))
    return bisect_left(prefix,random.randint(1,prefix[-1]))
''','O(n) preprocessing, O(log n) per pick','O(n)')
