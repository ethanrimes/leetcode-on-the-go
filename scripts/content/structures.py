from .base import category as G, card as C

G('Stacks, heaps & range queries','Maintain just enough order to answer the next query quickly.','Match the operation to the structure: LIFO nesting, monotone dominance, global extrema, or associative range aggregation.',['State what each stored index or value represents.','Account for amortized work, not just nested loop syntax.'],'design')
G('Stacks, heaps & range queries / Stack discipline','Resolve nested or adjacent structure in reverse arrival order.','Store pending context and finish it when the matching boundary arrives.',['Keep enough context to recover the previous state.'],'stack','Foundation')
C('Stacks, heaps & range queries / Stack discipline','Matching delimiters',20,'Foundation','Core','Check whether nested brackets close in the right order.','Push opening symbols; each closing symbol must match the most recent unmatched opener.','A valid prefix can still leave unmatched openers at the end.','Return whether a string containing only (), [], and {} is correctly balanced and nested.', ['([]{})'],True,'''
def solve(s):
    stack=[]; match={')':'(',']':'[','}':'{'}
    for ch in s:
        if ch in match:
            if not stack or stack.pop()!=match[ch]: return False
        else: stack.append(ch)
    return not stack
''','O(n)','O(n)')
C('Stacks, heaps & range queries / Stack discipline','Adjacent cancellation',1047,'Foundation','Useful','Removing a neighboring pair may expose another removable pair.','The stack holds the fully reduced prefix. Cancel a matching top or append the next character.','One left-to-right replacement pass misses cascading cancellations.','Repeatedly delete adjacent equal letter pairs until none remain; return the resulting string.', ['abbaca'],'ca','''
def solve(s):
    stack=[]
    for ch in s:
        if stack and stack[-1]==ch: stack.pop()
        else: stack.append(ch)
    return ''.join(stack)
''','O(n)','O(n)')
C('Stacks, heaps & range queries / Stack discipline','Nested decoding contexts',394,'Intermediate','Core','A nested expression repeats the result inside a bracket.','On an opening bracket save the current prefix and repeat count; on closing combine that frame with the decoded inner text.','Repeat counts can contain multiple digits.','Decode strings of the form k[segment], allowing nesting and literal letters. Input is well formed.', ['2[a3[b]]'],'abbbabbb','''
def solve(s):
    stack=[]; current=''; number=0
    for ch in s:
        if ch.isdigit(): number=number*10+int(ch)
        elif ch=='[': stack.append((current,number)); current=''; number=0
        elif ch==']': prefix,count=stack.pop(); current=prefix+current*count
        else: current+=ch
    return current
''','O(n + total intermediate decoded characters)','O(n + decoded output)')
C('Stacks, heaps & range queries / Stack discipline','Arithmetic precedence stack',227,'Intermediate','Useful','Multiplication and division bind more tightly than addition.','Resolve multiplication/division with the last term immediately; defer addition by storing signed terms.','Division truncates toward zero; Python // rounds down for negatives.','Evaluate a valid expression of nonnegative integers, spaces, and + − * /, without parentheses. Integer division truncates toward zero.', ['14-3/2'],13,'''
def solve(s):
    stack=[]; number=0; op='+'
    for ch in s+'+':
        if ch.isdigit(): number=number*10+int(ch)
        elif ch!=' ':
            if op=='+': stack.append(number)
            elif op=='-': stack.append(-number)
            elif op=='*': stack[-1]*=number
            else:
                old=stack.pop(); stack.append((abs(old)//number)*(1 if old>=0 else -1))
            op=ch; number=0
    return sum(stack)
''','O(n)','O(n)')
G('Stacks, heaps & range queries / Monotone structures','Discard candidates that can never beat a newer candidate.','Keep values in one direction of order; each pop must have a clear dominance or boundary meaning.',['Store indices when distances or expiration matter.','Choose strictness deliberately when duplicates exist.'],'monotonic-stack')
C('Stacks, heaps & range queries / Monotone structures','Next greater element',739,'Intermediate','Core','Each item waits for its first larger successor.','Keep unresolved indices in decreasing value order. A warmer temperature resolves every smaller stack top.','Equal temperatures do not resolve each other.','For each day, return how many days pass before a warmer temperature, or 0 if none.',[[30,40,35,50]],[1,2,1,0],'''
def solve(temperatures):
    stack=[]; answer=[0]*len(temperatures)
    for i,x in enumerate(temperatures):
        while stack and temperatures[stack[-1]]<x:
            j=stack.pop(); answer[j]=i-j
        stack.append(i)
    return answer
''','O(n)','O(n)')
C('Stacks, heaps & range queries / Monotone structures','Histogram span boundaries',84,'Advanced','Core','An element limits the height of its maximal rectangle.','Pop taller bars when a shorter bar arrives. The remaining stack top and current position bound the popped bar’s usable width.','Flush the stack with a sentinel zero height.','Given nonnegative bar heights of width one, return the largest rectangle area inside the histogram.',[[2,1,5,6,2,3]],10,'''
def solve(heights):
    stack=[]; best=0; a=heights+[0]
    for i,h in enumerate(a):
        while stack and a[stack[-1]]>h:
            height=a[stack.pop()]; left=stack[-1] if stack else -1
            best=max(best,height*(i-left-1))
        stack.append(i)
    return best
''','O(n)','O(n)')
C('Stacks, heaps & range queries / Monotone structures','Contribution counting with tie ownership',907,'Advanced','Useful','Sum a range statistic over every subarray.','Let each element own subarrays where it is the minimum; its contribution equals value × left choices × right choices.','Use a strict boundary on one side and non-strict on the other so equal minima are counted once.','Sum the minimum value of every nonempty subarray, modulo 1,000,000,007.',[[3,1,2,4]],17,'''
def solve(arr):
    stack=[]; total=0
    for right in range(len(arr)+1):
        while stack and (right==len(arr) or arr[stack[-1]]>=arr[right]):
            i=stack.pop(); left=stack[-1] if stack else -1
            total+=arr[i]*(i-left)*(right-i)
        stack.append(right)
    return total%1_000_000_007
''','O(n)','O(n)')
C('Stacks, heaps & range queries / Monotone structures','Monotone deque window extrema',239,'Advanced','Core','Query the maximum in each moving fixed-size window.','Keep candidate indices with decreasing values; expire old indices from the front and dominated values from the back.','A heap without deletion grows beyond the window size.','Return the maximum of every contiguous window of length k.',[[1,3,-1,-3,5,3,6,7],3],[3,3,5,5,6,7],'''
def solve(nums,k):
    from collections import deque
    q=deque(); answer=[]
    for i,x in enumerate(nums):
        while q and q[0]<=i-k: q.popleft()
        while q and nums[q[-1]]<=x: q.pop()
        q.append(i)
        if i>=k-1: answer.append(nums[q[0]])
    return answer
''','O(n)','O(k) excluding output')
C('Stacks, heaps & range queries / Monotone structures','Lexicographic monotone subsequence',316,'Intermediate','Useful','Keep one of each character with smallest lexicographic result.','Pop a larger previous character only if another copy remains later. Track membership separately.','Never discard the final available copy of a character.','Remove duplicate letters so every distinct letter occurs once and the remaining subsequence is lexicographically smallest.', ['cbacdcbc'],'acdb','''
def solve(s):
    last={ch:i for i,ch in enumerate(s)}; stack=[]; used=set()
    for i,ch in enumerate(s):
        if ch in used: continue
        while stack and stack[-1]>ch and last[stack[-1]]>i: used.remove(stack.pop())
        stack.append(ch); used.add(ch)
    return ''.join(stack)
''','O(n)','O(alphabet size)')
G('Stacks, heaps & range queries / Priority queues','Keep access to the next globally best candidate.','Choose a heap key that captures your ordering rule; use multiple heaps when a moving split is needed.',['Do not confuse heap order with total sorting.'],'heap-priority-queue')
C('Stacks, heaps & range queries / Priority queues','Bounded top-k heap',215,'Intermediate','Core','Retain only the best k values seen so far.','Maintain a min-heap of k largest values; its root is the kth largest after all input is processed.','The kth largest counts duplicates.','Return the kth largest value in an unsorted array, counting repeated values separately.',[[3,2,1,5,6,4],2],5,'''
def solve(nums,k):
    from heapq import heappush,heapreplace
    heap=[]
    for x in nums:
        if len(heap)<k: heappush(heap,x)
        elif x>heap[0]: heapreplace(heap,x)
    return heap[0]
''','O(n log k)','O(k)')
C('Stacks, heaps & range queries / Priority queues','Merge k sorted streams',373,'Intermediate','Useful','Enumerate smallest pair sums without enumerating the Cartesian product.','Start with the first element of each relevant row of the pair-sum matrix. Popping a pair advances only that row.','Limit initial rows to min(k,len(nums1)).','Given two sorted arrays, return k pairs [a,b] with smallest sums, or all pairs if fewer exist. Tied sums may be returned in any order.',[[1,7,11],[2,4,6],3],[[1,2],[1,4],[1,6]],'''
def solve(nums1,nums2,k):
    from heapq import heapify,heappop,heappush
    if not nums1 or not nums2: return []
    heap=[(nums1[i]+nums2[0],i,0) for i in range(min(k,len(nums1)))]; heapify(heap); out=[]
    while heap and len(out)<k:
        _,i,j=heappop(heap); out.append([nums1[i],nums2[j]])
        if j+1<len(nums2): heappush(heap,(nums1[i]+nums2[j+1],i,j+1))
    return out
''','O(k log(min(k,m)+1))','O(min(k,m)) excluding output')
C('Stacks, heaps & range queries / Priority queues','Two heaps around the median',295,'Advanced','Core','Maintain a changing median as values arrive.','Use a max-heap for the lower half and a min-heap for the upper half. Keep lower half equal in size or one larger.','Balance size after restoring ordering.','Insert each stream value and report the median after each insertion. This study wrapper represents repeated addNum/findMedian operations.',[[5,1,9,2]],[5,3.0,5,3.5],'''
def solve(stream):
    from heapq import heappush,heappop
    low=[]; high=[]; answer=[]
    for x in stream:
        heappush(low,-x); heappush(high,-heappop(low))
        if len(high)>len(low): heappush(low,-heappop(high))
        answer.append(-low[0] if len(low)>len(high) else (-low[0]+high[0])/2)
    return answer
''','O(n log n) total','O(n)')
G('Stacks, heaps & range queries / Mutable range queries','Summarize ranges while values change.','Use an associative operation and decompose updates or queries into logarithmically many blocks.',['A Fenwick tree needs invertible prefix aggregation for arbitrary range sums.','A segment tree supports broader associative operations.'],'segment-tree','Advanced')
C('Stacks, heaps & range queries / Mutable range queries','Fenwick tree point updates',307,'Advanced','Core','Interleave point assignments and interval-sum queries.','Store partial sums at one-based indices. Walk ancestors with i+=i&−i for updates and i−=i&−i for prefix sums.','An assignment is an update by new−old, not by new.','Given nums and operations ["update",index,value] or ["sumRange",left,right], return results for inclusive range-sum queries.',[[1,3,5],[['sumRange',0,2],['update',1,2],['sumRange',0,2]]],[9,8],'''
def solve(nums,operations):
    n=len(nums); bit=[0]*(n+1); values=nums[:]
    def add(i,delta):
        i+=1
        while i<=n: bit[i]+=delta; i+=i&-i
    def prefix(i):
        total=0
        while i>0: total+=bit[i]; i-=i&-i
        return total
    for i,x in enumerate(nums): add(i,x)
    answer=[]
    for op,a,b in operations:
        if op=='update': add(a,b-values[a]); values[a]=b
        else: answer.append(prefix(b+1)-prefix(a))
    return answer
''','O((n+q) log n)','O(n)')
C('Stacks, heaps & range queries / Mutable range queries','Iterative segment tree',307,'Advanced','Useful','Answer associative range queries with point updates.','Place leaves in the second half of an array and combine parents. Query [left,right) by consuming exposed odd boundaries.','Convert an inclusive right endpoint to exclusive before querying.','Given nums and update/sumRange operations, return all inclusive range sums.',[[1,3,5],[['sumRange',0,2],['update',1,2],['sumRange',0,2]]],[9,8],'''
def solve(nums,operations):
    n=len(nums); tree=[0]*n+nums[:]
    for i in range(n-1,0,-1): tree[i]=tree[2*i]+tree[2*i+1]
    answer=[]
    for op,a,b in operations:
        if op=='update':
            i=a+n; tree[i]=b
            while i>1: i//=2; tree[i]=tree[2*i]+tree[2*i+1]
        else:
            left,right=a+n,b+n+1; total=0
            while left<right:
                if left%2: total+=tree[left]; left+=1
                if right%2: right-=1; total+=tree[right]
                left//=2; right//=2
            answer.append(total)
    return answer
''','O(n + q log n)','O(n)')
C('Stacks, heaps & range queries / Mutable range queries','Coordinate compression and inversion counts',315,'Advanced','Useful','Compare ranks in a large or sparse value domain.','Compress values to sorted ranks, scan right to left, query counts of smaller ranks, then insert the current rank.','Query strictly smaller ranks so equal values are excluded.','For each array element return how many later elements are strictly smaller.',[[5,2,6,1]],[2,1,1,0],'''
def solve(nums):
    rank={v:i+1 for i,v in enumerate(sorted(set(nums)))}; bit=[0]*(len(rank)+1); out=[]
    for x in reversed(nums):
        i=rank[x]-1; total=0
        while i: total+=bit[i]; i-=i&-i
        out.append(total); i=rank[x]
        while i<len(bit): bit[i]+=1; i+=i&-i
    return out[::-1]
''','O(n log n)','O(n)')
G('Stacks, heaps & range queries / Data structure design','Combine structures to satisfy several operation contracts.','Specify per-operation invariants, then compose structures whose strengths cover each requirement.',['Separate interface behavior from representation.'],'design')
C('Stacks, heaps & range queries / Data structure design','LRU order plus key lookup',146,'Intermediate','Core','Evict the least recently used key in constant time.','Pair key lookup with recency ordering; every get and update moves an entry to the most-recent end. OrderedDict exposes the same combined behavior.','Updating an existing key also changes recency.','Simulate a capacity-bounded LRU cache. Operations are ["put",key,value] or ["get",key]; return get results, using −1 for absent keys.',[2,[['put',1,7],['put',2,8],['get',1],['put',3,9],['get',2]]],[7,-1],'''
def solve(capacity,operations):
    from collections import OrderedDict
    cache=OrderedDict(); out=[]
    for op in operations:
        key=op[1]
        if op[0]=='get':
            out.append(cache.get(key,-1))
            if key in cache: cache.move_to_end(key)
        else:
            cache[key]=op[2]; cache.move_to_end(key)
            if len(cache)>capacity: cache.popitem(last=False)
    return out
''','O(1) per operation expected','O(capacity)')
C('Stacks, heaps & range queries / Data structure design','Min stack with aggregate snapshots',155,'Foundation','Core','Query the current minimum while using ordinary stack operations.','Store each value together with the minimum of the stack prefix ending there.','Duplicate minima need independent snapshots.','Simulate push, pop, top, and getMin on a nonempty-when-queried stack; return top/getMin query values.',[[['push',3],['push',1],['getMin'],['pop'],['top'],['getMin']]],[1,3,3],'''
def solve(operations):
    stack=[]; out=[]
    for op in operations:
        if op[0]=='push':
            x=op[1]; stack.append((x,min(x,stack[-1][1]) if stack else x))
        elif op[0]=='pop': stack.pop()
        elif op[0]=='top': out.append(stack[-1][0])
        else: out.append(stack[-1][1])
    return out
''','O(1) per operation','O(n)')
C('Stacks, heaps & range queries / Data structure design','Amortized queue using two stacks',232,'Foundation','Useful','Provide FIFO behavior with LIFO primitives.','Push to an incoming stack; move all items to an outgoing stack only when the outgoing stack becomes empty.','Moving on every operation destroys the amortized constant-time bound.','Simulate push, pop, peek, and empty operations for a queue. Return results of every non-push operation.',[[['push',1],['push',2],['peek'],['pop'],['empty']]],[1,1,False],'''
def solve(operations):
    incoming=[]; outgoing=[]; out=[]
    for op in operations:
        if op[0]=='push': incoming.append(op[1]); continue
        if op[0]=='empty': out.append(not incoming and not outgoing); continue
        if not outgoing:
            while incoming: outgoing.append(incoming.pop())
        out.append(outgoing.pop() if op[0]=='pop' else outgoing[-1])
    return out
''','O(1) amortized per operation','O(n)')

C('Stacks, heaps & range queries / Monotone structures','Circular next-greater scan',503,'Intermediate','Useful','An unresolved item may find its successor after the end of an array.','Scan indices twice modulo n, but push unresolved indices only during the first lap; the second lap only resolves them.','Pushing on both laps duplicates candidates and obscures the one-answer-per-index invariant.','For each value in a circular array, return the first greater value encountered moving right, or -1.',[[1,2,1]],[2,-1,2],'''
def solve(nums):
    n = len(nums)
    answer = [-1] * n
    pending = []
    for step in range(2 * n):
        i = step % n
        while pending and nums[pending[-1]] < nums[i]:
            answer[pending.pop()] = nums[i]
        if step < n: pending.append(i)
    return answer
''','O(n)','O(n)')
C('Stacks, heaps & range queries / Monotone structures','Greedy digit removal',402,'Intermediate','Useful','Discard digits to make the smallest remaining number.','While removals remain, a smaller incoming digit can replace a larger previous digit. Then remove any remaining quota from the tail.','Leading zeros must be stripped, and an empty result is zero.','Remove exactly k digits from a decimal string to produce the smallest possible nonnegative integer string.', ['1432219',3],'1219','''
def solve(num, k):
    digits = []
    for ch in num:
        while k and digits and digits[-1] > ch:
            digits.pop()
            k -= 1
        digits.append(ch)
    if k: digits = digits[:-k]
    return ''.join(digits).lstrip('0') or '0'
''','O(n)','O(n)')
