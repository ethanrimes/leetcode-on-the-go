from .base import category as G, card as C

G('Arrays & hashing','Turn repeated scans into small, reusable summaries.','Choose what information each prefix must preserve: membership, counts, positions, or a cumulative value.',['Check duplicates and negative values.','Decide whether order matters before sorting.'],'array', 'Foundation')
G('Arrays & hashing / Lookup & counting','Remember exactly what later elements need.','Use a hash map to answer a previously linear query in expected constant time.',['Check before inserting when an element must not match itself.'],'hash-table','Foundation')
C('Arrays & hashing / Lookup & counting','Complement lookup',1,'Foundation','Core','A pair must add to a target.','For each value x, look for target − x among earlier values. Store indices only after the lookup.','Inserting first can reuse the same index.','Return the two different indices whose values sum to target. Exactly one valid pair exists.',[[4,8,2,11],10],[1,2],'''
def solve(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
''','O(n)','O(n)','At least two integers; exactly one answer.')
C('Arrays & hashing / Lookup & counting','Frequency signatures',49,'Foundation','Core','Group items that differ only by ordering.','Use the sorted characters as a stable signature and collect equal signatures together.','A set loses multiplicity: abb and ab are different.','Group strings that contain the same letters with the same multiplicities. Group order is irrelevant.',[['eat','tea','bat']],[['eat','tea'],['bat']],'''
def solve(strs):
    groups = {}
    for s in strs:
        key = ''.join(sorted(s))
        groups.setdefault(key, []).append(s)
    return list(groups.values())
''','O(n k log k), k = longest string','O(nk)', pseudocode='''
groups ← empty map

for each word in words:
    letters ← sort(characters(word))
    signature ← join(letters)

    if signature is not in groups:
        groups[signature] ← empty list

    append word to groups[signature]

return all lists stored in groups
''', pseudocode_example='''
"eat" → "aet" → ["eat"]
"tea" → "aet" → ["eat", "tea"]
"abb" → "abb" → ["abb"]
"ab"  → "ab"  → ["ab"]

Same signature → same group.
Repeated letters stay in the signature.
''')
C('Arrays & hashing / Lookup & counting','Sequence boundary detection',128,'Intermediate','Core','Find a consecutive run in unsorted data.','Only grow a run from x when x−1 is absent. Each distinct value is visited within one run.','Starting a walk from every value produces quadratic work.','Return the length of the longest run of consecutive integer values; input order does not matter.',[[9,1,4,3,2]],4,'''
def solve(nums):
    values = set(nums)
    best = 0
    for x in values:
        if x - 1 not in values:
            y = x
            while y in values:
                y += 1
            best = max(best, y - x)
    return best
''','O(n) expected','O(n)')
G('Arrays & hashing / Prefix & difference','Exchange repeated range work for cumulative state.','Define a prefix at an exclusive boundary; obtain a range by subtracting two prefixes.',['Seed the empty prefix.','Difference arrays invert the direction: record changes, then accumulate.'],'prefix-sum','Foundation')
C('Arrays & hashing / Prefix & difference','Prefix sum with frequency map',560,'Intermediate','Core','Count subarrays with a given sum, including negative values.','A subarray ending at this prefix has sum k when an earlier prefix equals current−k. Count earlier prefixes before adding the current one.','A sliding window is not monotone when negative values are allowed.','Count contiguous, nonempty subarrays whose sum equals k.',[[2,-1,2,1],3],2,'''
def solve(nums, k):
    counts = {0: 1}
    prefix = answer = 0
    for x in nums:
        prefix += x
        answer += counts.get(prefix - k, 0)
        counts[prefix] = counts.get(prefix, 0) + 1
    return answer
''','O(n) expected','O(n)')
C('Arrays & hashing / Prefix & difference','Remainder classes',974,'Intermediate','Useful','A range sum must be divisible by k.','Two prefix sums with the same remainder differ by a multiple of k.','Normalize modulo in languages where negative remainders are possible.','Count nonempty subarrays whose sum is divisible by positive integer k.',[[3,1,2,-3],3],6,'''
def solve(nums, k):
    counts = {0: 1}
    rem = answer = 0
    for x in nums:
        rem = (rem + x) % k
        answer += counts.get(rem, 0)
        counts[rem] = counts.get(rem, 0) + 1
    return answer
''','O(n)','O(min(n,k))')
C('Arrays & hashing / Prefix & difference','Prefix and suffix products',238,'Intermediate','Core','Each answer excludes exactly one element.','Write left products into the output, then multiply by a running right product.','Division breaks when zeros appear.','For each position, return the product of every other element without division.',[[2,3,0,4]],[0,0,24,0],'''
def solve(nums):
    out = [1] * len(nums)
    left = 1
    for i, x in enumerate(nums):
        out[i] = left
        left *= x
    right = 1
    for i in range(len(nums) - 1, -1, -1):
        out[i] *= right
        right *= nums[i]
    return out
''','O(n)','O(1) auxiliary, excluding output')
C('Arrays & hashing / Prefix & difference','Range updates with differences',1109,'Intermediate','Useful','Many intervals add an amount to every covered position.','Add at the start and subtract immediately after the end, then take a prefix sum once.','Convert the one-based booking indices carefully.','Each booking [first,last,seats] adds seats to every flight in that inclusive one-based range. Return totals for n flights.',[[[1,2,5],[2,3,7]],3],[5,12,7],'''
def solve(bookings, n):
    diff = [0] * (n + 1)
    for first, last, seats in bookings:
        diff[first - 1] += seats
        diff[last] -= seats
    for i in range(1, n):
        diff[i] += diff[i - 1]
    return diff[:n]
''','O(n + bookings)','O(n)')
C('Arrays & hashing / Prefix & difference','Two-dimensional prefix sums',1314,'Intermediate','Useful','Many rectangular sums on the same matrix.','Pad the prefix matrix with zeros; use inclusion–exclusion for each clipped rectangle.','Subtract the overlap only once when building, add it back when querying.','For each cell of mat, sum all cells within k rows and k columns, clipped to the matrix.',[[[1,2],[3,4]],1],[[10,10],[10,10]],'''
def solve(mat, k):
    m, n = len(mat), len(mat[0])
    p = [[0] * (n + 1) for _ in range(m + 1)]
    for r in range(m):
        for c in range(n):
            p[r+1][c+1] = mat[r][c] + p[r][c+1] + p[r+1][c] - p[r][c]
    out = [[0] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            a, b = max(0, r-k), max(0, c-k)
            x, y = min(m, r+k+1), min(n, c+k+1)
            out[r][c] = p[x][y] - p[a][y] - p[x][b] + p[a][b]
    return out
''','O(mn)','O(mn)')
G('Arrays & hashing / In-place structure','Use positions as part of the representation.','Establish which region is already correct and grow it without invalidating previous work.',['Save values before overwriting.','Prove swaps terminate.'],'array')
C('Arrays & hashing / In-place structure','Index placement',41,'Advanced','Useful','Values map naturally to positions 1 through n.','Repeatedly place each in-range value x at index x−1. The first mismatch identifies the missing positive.','Check the destination value to avoid infinite swaps with duplicates.','Return the smallest missing positive integer using constant auxiliary space.',[[3,4,-1,1]],2,'''
def solve(nums):
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i]-1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i, x in enumerate(nums):
        if x != i + 1:
            return i + 1
    return n + 1
''','O(n)','O(1)')
C('Arrays & hashing / In-place structure','Boyer–Moore cancellation',169,'Foundation','Useful','One value is guaranteed to occupy more than half the positions.','Cancel unequal pairs; the strict majority survives as the candidate.','Without the majority guarantee, verify the candidate in a second pass.','Return the value occurring more than floor(n/2) times. Such a value is guaranteed.',[[2,1,2,3,2]],2,'''
def solve(nums):
    candidate, count = None, 0
    for x in nums:
        if count == 0:
            candidate = x
        count += 1 if x == candidate else -1
    return candidate
''','O(n)','O(1)')
C('Arrays & hashing / In-place structure','Matrix boundary simulation',54,'Foundation','Useful','Visit a matrix in concentric rectangular layers.','Maintain four unvisited boundaries; consume the top, right, bottom, then left side.','Recheck boundaries before the bottom and left passes on thin matrices.','Return all matrix entries in clockwise spiral order starting at the top-left corner.',[[[1,2,3],[4,5,6]]],[1,2,3,6,5,4],'''
def solve(matrix):
    top, bottom, left, right = 0, len(matrix)-1, 0, len(matrix[0])-1
    out = []
    while top <= bottom and left <= right:
        out.extend(matrix[top][left:right+1]); top += 1
        for r in range(top, bottom+1): out.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            out.extend(matrix[bottom][left:right+1][::-1]); bottom -= 1
        if left <= right:
            for r in range(bottom, top-1, -1): out.append(matrix[r][left])
            left += 1
    return out
''','O(mn)','O(1) excluding output','Nonempty rectangular matrix.')

G('Two pointers & windows','Make a pair of boundaries do the work of nested loops.','Find a monotone reason to advance one boundary without missing an answer.',['Write what makes a window valid.','Distinguish maximizing a valid window from minimizing a covering window.'],'two-pointers','Foundation')
G('Two pointers & windows / Opposing & forward pointers','Exploit sorted order or independent read/write positions.','Eliminate a candidate region with each movement.',['Prove why moving one pointer cannot discard a better answer.'],'two-pointers','Foundation')
C('Two pointers & windows / Opposing & forward pointers','Opposing pointers on sorted values',167,'Foundation','Core','A sorted pair must meet a target.','When the sum is too small, increase the left value; when too large, decrease the right value.','This monotonic argument requires sorted input.','In a sorted array with exactly one solution, return one-based indices of two distinct values summing to target.',[[1,4,6,9],10],[1,4],'''
def solve(numbers, target):
    left, right = 0, len(numbers)-1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target: return [left+1, right+1]
        if total < target: left += 1
        else: right -= 1
''','O(n)','O(1)')
C('Two pointers & windows / Opposing & forward pointers','Fix one, solve two-sum',15,'Intermediate','Core','Find unique triples with a fixed total.','Sort, fix the first value, then solve two-sum on the suffix; skip equal values at each decision boundary.','Deduplicate values, not original indices.','Return each distinct triple of values that sums to zero. Triple and result order are irrelevant.',[[-2,0,1,1,2]],[[-2,0,2],[-2,1,1]],'''
def solve(nums):
    nums = sorted(nums); out = []
    for i in range(len(nums)-2):
        if i and nums[i] == nums[i-1]: continue
        left, right = i+1, len(nums)-1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s < 0: left += 1
            elif s > 0: right -= 1
            else:
                out.append([nums[i], nums[left], nums[right]])
                left += 1; right -= 1
                while left < right and nums[left] == nums[left-1]: left += 1
                while left < right and nums[right] == nums[right+1]: right -= 1
    return out
''','O(n²)','O(n) for sorting copy, excluding output')
C('Two pointers & windows / Opposing & forward pointers','Move the limiting boundary',11,'Intermediate','Core','Area depends on width and the shorter endpoint.','The shorter wall limits the area. Holding it while narrowing the interval cannot improve the answer, so move it.','Moving the taller wall has no such elimination guarantee.','Choose two vertical lines to maximize the water container area: distance times the smaller height.',[[2,7,3,6]],12,'''
def solve(height):
    left, right, best = 0, len(height)-1, 0
    while left < right:
        best = max(best, (right-left)*min(height[left], height[right]))
        if height[left] <= height[right]: left += 1
        else: right -= 1
    return best
''','O(n)','O(1)')
C('Two pointers & windows / Opposing & forward pointers','Read/write compaction',283,'Foundation','Core','Keep selected elements in order, in place.','Write each nonzero element into the next kept position, then fill the suffix with zeros.','The write pointer never passes the read pointer.','Move every zero to the end while preserving the relative order of nonzero values. Return the mutated array for study.',[[0,4,0,2]],[4,2,0,0],'''
def solve(nums):
    write = 0
    for x in nums:
        if x != 0:
            nums[write] = x; write += 1
    for i in range(write, len(nums)): nums[i] = 0
    return nums
''','O(n)','O(1)')
C('Two pointers & windows / Opposing & forward pointers','Three-way partition',75,'Intermediate','Useful','Separate three value classes in one pass.','Maintain [0,low) as zeros, [low,mid) as ones, and (high,n) as twos. Classify the unknown at mid.','After swapping with high, the new mid value is still unclassified.','Sort an array containing only 0, 1, and 2 in place; return it for study.',[[2,0,1,2,0]],[0,0,1,2,2],'''
def solve(nums):
    low = mid = 0; high = len(nums)-1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1; mid += 1
        elif nums[mid] == 2:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
        else: mid += 1
    return nums
''','O(n)','O(1)')
G('Two pointers & windows / Sliding windows','Reuse the work shared by adjacent contiguous ranges.','Expand the right boundary, update summary state, and shrink from the left according to validity.',['Each element should enter and leave at most once.','Use prefix sums instead if validity is not monotone.'],'sliding-window')
C('Two pointers & windows / Sliding windows','Fixed-length rolling window',643,'Foundation','Core','Optimize over all contiguous ranges of exactly k elements.','Start with one complete window; each shift adds the entering value and removes the departing value.','Initialize from real data so all-negative arrays work.','Return the largest average of any contiguous subarray of length k.',[[-2,4,6,-1],2],5.0,'''
def solve(nums, k):
    total = best = sum(nums[:k])
    for i in range(k, len(nums)):
        total += nums[i] - nums[i-k]
        best = max(best, total)
    return best / k
''','O(n)','O(k) for initial slice; O(1) if summed by index','1 ≤ k ≤ array length.')
C('Two pointers & windows / Sliding windows','Longest valid window',3,'Intermediate','Core','Find the longest range without duplicate symbols.','Track the last occurrence of each character and jump the left boundary beyond a repeated occurrence.','Never move left backwards when the repeat was outside the current window.','Return the length of the longest substring containing no repeated character.', ['abcaef'],5,'''
def solve(s):
    last = {}; left = best = 0
    for right, ch in enumerate(s):
        left = max(left, last.get(ch, -1)+1)
        last[ch] = right
        best = max(best, right-left+1)
    return best
''','O(n)','O(alphabet size)')
C('Two pointers & windows / Sliding windows','Shortest covering window',76,'Advanced','Core','Find the smallest substring satisfying a multiset demand.','Count missing required characters. Expand until all demands are met, then shrink while preserving coverage.','Repeated characters in the target require repeated occurrences in the window.','Return a shortest substring of s containing every character of t with its multiplicity; return empty if impossible.', ['cabefgecda','ca'],'ca','''
def solve(s, t):
    from collections import Counter
    if not t: return ''
    need = Counter(t); missing = len(t); left = 0; best = (0, len(s)+1)
    for right, ch in enumerate(s):
        if need[ch] > 0: missing -= 1
        need[ch] -= 1
        while missing == 0:
            if right-left+1 < best[1]-best[0]: best = (left, right+1)
            need[s[left]] += 1
            if need[s[left]] > 0: missing += 1
            left += 1
    return '' if best[1] > len(s) else s[best[0]:best[1]]
''','O(n + m)','O(alphabet size)')
C('Two pointers & windows / Sliding windows','Exactly k via at most k',992,'Advanced','Useful','Count windows with exactly k distinct values.','Count at most k and subtract at most k−1. For a fixed right endpoint, every suffix of a valid window is valid.','Add right−left+1, not just one window.','Count nonempty contiguous subarrays containing exactly k distinct integers.',[[1,2,1,3],2],4,'''
def solve(nums, k):
    def at_most(limit):
        if limit < 0: return 0
        counts = {}; left = total = 0
        for right, x in enumerate(nums):
            counts[x] = counts.get(x, 0)+1
            while len(counts) > limit:
                y = nums[left]; counts[y] -= 1; left += 1
                if counts[y] == 0: del counts[y]
            total += right-left+1
        return total
    return at_most(k) - at_most(k-1)
''','O(n) expected','O(k)')
C('Two pointers & windows / Sliding windows','Replacement-budget window',424,'Intermediate','Useful','A window may violate a property up to k times.','A window can become uniform when its length minus its highest character frequency is at most k. Track a nondecreasing maximum frequency.','A stale maximum is safe for the maximum length, but not for reporting every valid window.','With at most k character replacements, find the longest substring of an uppercase string that can be made uniform.', ['AABABBA',1],4,'''
def solve(s, k):
    counts = {}; left = top = best = 0
    for right, ch in enumerate(s):
        counts[ch] = counts.get(ch, 0)+1; top = max(top, counts[ch])
        if right-left+1-top > k:
            counts[s[left]] -= 1; left += 1
        best = max(best, right-left+1)
    return best
''','O(n)','O(26)')

G('Binary search','Search for the boundary where a monotone predicate changes.','Define the search interval and the meaning of true before writing the loop.',['A lower-bound loop uses [left,right).','Prove monotonicity when searching answers.'],'binary-search','Foundation')
G('Binary search / Ordered positions','Discard half of an ordered search space.','Maintain all possible answers inside the current interval.',['Use consistent inclusive or half-open boundaries.'],'binary-search','Foundation')
C('Binary search / Ordered positions','Lower bound',35,'Foundation','Core','Locate the first value not smaller than target.','Maintain a half-open interval; values before left are smaller, values at or beyond right are large enough.','The insertion position may equal the array length.','Return the insertion index of target in a sorted array with distinct values.',[[1,4,7,9],6],2,'''
def solve(nums, target):
    left, right = 0, len(nums)
    while left < right:
        mid = (left+right)//2
        if nums[mid] < target: left = mid+1
        else: right = mid
    return left
''','O(log n)','O(1)')
C('Binary search / Ordered positions','Rotated sorted search',33,'Intermediate','Core','A sorted array has one rotation break.','At least one half is sorted. Check whether the target lies within that half before choosing a side.','The standard single-pass decision assumes distinct values.','Return the index of target in a rotated sorted array of distinct integers, or −1.',[[6,8,1,2,4],2],3,'''
def solve(nums, target):
    left, right = 0, len(nums)-1
    while left <= right:
        mid = (left+right)//2
        if nums[mid] == target: return mid
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]: right = mid-1
            else: left = mid+1
        else:
            if nums[mid] < target <= nums[right]: left = mid+1
            else: right = mid-1
    return -1
''','O(log n)','O(1)')
C('Binary search / Ordered positions','Peak by slope',162,'Intermediate','Useful','Find any local maximum without requiring global sorting.','If the next value is higher, a peak exists to the right; otherwise one exists at mid or to the left.','The guarantee uses unequal adjacent values and imaginary −infinity at both ends.','Return the index of any element greater than its neighbors. Adjacent values differ; outside neighbors are treated as −infinity.',[[1,3,5,2]],2,'''
def solve(nums):
    left, right = 0, len(nums)-1
    while left < right:
        mid = (left+right)//2
        if nums[mid] < nums[mid+1]: left = mid+1
        else: right = mid
    return left
''','O(log n)','O(1)')
C('Binary search / Ordered positions','Partition two sorted arrays',4,'Advanced','Specialist','Find an order statistic across two sorted sequences.','Binary search a partition in the shorter array. Match its complement so the left half has the required size, then enforce both crossing inequalities.','Use sentinels at empty partitions and search the shorter input.','Return the median of two sorted arrays whose combined length is positive.',[[1,5],[2,3,7]],3,'''
def solve(a, b):
    if len(a) > len(b): return solve(b, a)
    m, n = len(a), len(b); left, right = 0, m
    while left <= right:
        i = (left+right)//2; j = (m+n+1)//2-i
        al = a[i-1] if i else float('-inf')
        ar = a[i] if i < m else float('inf')
        bl = b[j-1] if j else float('-inf')
        br = b[j] if j < n else float('inf')
        if al <= br and bl <= ar:
            if (m+n)%2: return max(al, bl)
            return (max(al, bl)+min(ar, br))/2
        if al > br: right = i-1
        else: left = i+1
''','O(log min(m,n))','O(1)')
G('Binary search / Search on the answer','Optimize a value by answering a feasibility question.','Choose bounds that contain an answer; binary search the first feasible or last feasible value.',['Test the feasibility predicate independently.','Integer division often needs ceiling.'],'binary-search')
C('Binary search / Search on the answer','Minimum feasible rate',875,'Intermediate','Core','Increasing a rate can only make completion easier.','For a trial rate, sum ceil(pile/rate). Search for the smallest rate whose total hours fits the budget.','Use integer ceiling division rather than floating-point rounding.','Each hour, eat up to k items from one pile. Find the minimum integer k that finishes all piles within h hours.',[[4,8,12],6],4,'''
def solve(piles, h):
    left, right = 1, max(piles)
    while left < right:
        mid = (left+right)//2
        if sum((x+mid-1)//mid for x in piles) <= h: right = mid
        else: left = mid+1
    return left
''','O(n log max(piles))','O(1)','Positive piles; h is at least the number of piles.')
C('Binary search / Search on the answer','Minimize the maximum partition',410,'Advanced','Core','Split a sequence into a fixed number of contiguous groups.','For a proposed maximum sum, greedily pack each group. Search the smallest cap needing at most k groups.','Nonnegative values make greedy feasibility monotone.','Partition a nonnegative array into k nonempty contiguous parts, minimizing the largest part sum.',[[4,2,7,3],2],10,'''
def solve(nums, k):
    left, right = max(nums), sum(nums)
    while left < right:
        mid = (left+right)//2; groups = 1; total = 0
        for x in nums:
            if total+x > mid: groups += 1; total = 0
            total += x
        if groups <= k: right = mid
        else: left = mid+1
    return left
''','O(n log sum(nums))','O(1)','1 ≤ k ≤ n; all values are nonnegative.')
C('Binary search / Search on the answer','Maximize the minimum separation',1552,'Intermediate','Useful','Choose locations to maximize the closest pair distance.','Sort positions, greedily place the next ball at the earliest feasible point, and search the largest feasible distance.','Use an upper midpoint when keeping a feasible lower bound.','Place m balls in distinct given positions so their minimum pairwise distance is as large as possible.',[[1,2,4,8,9],3],3,'''
def solve(position, m):
    position = sorted(position); left, right = 0, position[-1]-position[0]
    while left < right:
        mid = (left+right+1)//2; count = 1; last = position[0]
        for x in position[1:]:
            if x-last >= mid: count += 1; last = x
        if count >= m: left = mid
        else: right = mid-1
    return left
''','O(n log n + n log range)','O(n)')

C('Binary search / Ordered positions','Equal-value boundaries',34,'Intermediate','Core','Find the full interval occupied by a target in sorted data.','Run lower bound twice: once for target and once for the first value greater than target. The answer lies between them.','An arbitrary binary-search hit does not identify either boundary.','Return the first and last index of target in a sorted array, or [-1,-1] if absent.',[[1,2,2,2,4],2],[1,3],'''
def solve(nums, target):
    def lower(x):
        lo, hi = 0, len(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < x: lo = mid + 1
            else: hi = mid
        return lo
    first = lower(target)
    if first == len(nums) or nums[first] != target: return [-1, -1]
    return [first, lower(target + 1) - 1]
''','O(log n)','O(1)')
C('Binary search / Ordered positions','Rotated minimum boundary',153,'Intermediate','Useful','Find the pivot value in a rotated sorted array.','Compare mid to the rightmost candidate; a larger mid lies before the wrap, otherwise the minimum remains at mid or left of it.','This strict comparison assumes distinct values.','Return the smallest value in a nonempty rotated sorted array of distinct integers.',[[4,5,6,1,2,3]],1,'''
def solve(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]: lo = mid + 1
        else: hi = mid
    return nums[lo]
''','O(log n)','O(1)')
C('Two pointers & windows / Sliding windows','Minimum window with positive sums',209,'Intermediate','Core','Reach a sum threshold with as few consecutive elements as possible.','With positive values, removing from the left strictly lowers the sum; shrink every valid window before advancing right.','This shrink rule fails when negatives can later restore the sum.','Return the minimum length of a contiguous subarray whose sum is at least target, or 0 if none exists. All nums are positive.',[7,[2,3,1,2,4,3]],2,'''
def solve(target, nums):
    left = total = 0
    best = len(nums) + 1
    for right, value in enumerate(nums):
        total += value
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best > len(nums) else best
''','O(n)','O(1)')
C('Arrays & hashing / Prefix & difference','Balanced binary prefix states',525,'Intermediate','Useful','Find the longest interval with equal numbers of two symbols.','Treat zero as -1 and one as +1; equal transformed prefixes delimit a balanced interval. Save each prefix’s earliest position.','Overwriting the earliest position can only shorten later intervals.','Return the maximum length of a contiguous subarray with equally many 0s and 1s.',[[0,1,0,0,1,1]],6,'''
def solve(nums):
    first = {0: -1}
    balance = best = 0
    for i, value in enumerate(nums):
        balance += 1 if value else -1
        if balance in first: best = max(best, i - first[balance])
        else: first[balance] = i
    return best
''','O(n)','O(n)')
