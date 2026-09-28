from .base import category as G, card as C

G('Dynamic programming','Solve overlapping subproblems once, with a state that remembers only what the future needs.','Define state in a sentence, list choices, write the recurrence, and establish base cases before choosing memoization or tabulation.',['Estimate states × transitions.','Compress memory only after verifying the full recurrence.'],'dynamic-programming')
G('Dynamic programming / Linear sequences','Move through a sequence while retaining a small summary of its prefix.','Describe what a solution ending at i needs from earlier positions.',['Distinguish ending at i from best anywhere through i.'],'dynamic-programming')
C('Dynamic programming / Linear sequences','Fibonacci-style counting',70,'Foundation','Core','The last move has one of a few fixed lengths.','Count ways to arrive at a step by adding counts for each possible previous step.','The empty prefix contributes one way.','Count ways to climb n steps when every move advances one or two steps.',[5],8,'''
def solve(n):
    a = b = 1
    for _ in range(n): a, b = b, a+b
    return a
''','O(n)','O(1)','n is a positive integer.')
C('Dynamic programming / Linear sequences','Take or skip adjacent items',198,'Foundation','Core','Choosing an item forbids its neighbor.','The best prefix either skips the current value or takes it plus the best prefix ending two positions earlier.','Save both old states before updating.','Choose nonadjacent values from a nonnegative array to maximize their sum.',[[3,2,6,4]],9,'''
def solve(nums):
    prev2 = prev1 = 0
    for x in nums: prev2, prev1 = prev1, max(prev1, prev2+x)
    return prev1
''','O(n)','O(1)')
C('Dynamic programming / Linear sequences','Break a cycle into paths',213,'Intermediate','Useful','The first and last choices conflict on a ring.','Solve two paths: exclude the first item, or exclude the last. Every valid selection belongs to at least one case.','Handle a one-item ring separately.','Choose a maximum-sum subset of nonadjacent nonnegative values arranged in a circle.',[[2,7,3,8]],15,'''
def solve(nums):
    if len(nums) == 1: return nums[0]
    def linear(start, end):
        a = b = 0
        for i in range(start, end): a, b = b, max(b, a+nums[i])
        return b
    return max(linear(0, len(nums)-1), linear(1, len(nums)))
''','O(n)','O(1)')
C('Dynamic programming / Linear sequences','Kadane: extend or restart',53,'Foundation','Core','Find the best contiguous sum.','A best subarray ending here either starts here or extends the previous best ending position.','Initialize from the first value, not zero, when the answer must be nonempty.','Return the maximum sum of a nonempty contiguous subarray.',[[-4,3,-1,5,-6]],7,'''
def solve(nums):
    ending = best = nums[0]
    for x in nums[1:]:
        ending = max(x, ending+x); best = max(best, ending)
    return best
''','O(n)','O(n) due to slice; O(1) with index iteration')
C('Dynamic programming / Linear sequences','Track both extrema',152,'Intermediate','Useful','A negative multiplier swaps the best and worst states.','Keep both minimum and maximum products ending at each position; update from both old extrema.','Zero naturally restarts both states.','Return the largest product of a nonempty contiguous subarray.',[[-2,3,-4]],24,'''
def solve(nums):
    low = high = best = nums[0]
    for i in range(1, len(nums)):
        x = nums[i]; a, b = low*x, high*x
        low, high = min(x, a, b), max(x, a, b)
        best = max(best, high)
    return best
''','O(n)','O(1)')
C('Dynamic programming / Linear sequences','Count by reachable length',2466,'Intermediate','Core','A sequence is built by appending fixed-size blocks.','Let dp[length] count constructions of exactly that length. Add counts from length−zero and length−one, then sum the permitted interval.','If both block lengths match, the two choices still represent different strings.','Build binary strings by appending either zero zeroes or one ones. Count distinct strings with lengths in [low,high], modulo 1,000,000,007.',[2,3,1,2],5,'''
def solve(low, high, zero, one):
    mod = 1_000_000_007; dp = [0]*(high+1); dp[0] = 1
    for length in range(1, high+1):
        if length >= zero: dp[length] += dp[length-zero]
        if length >= one: dp[length] += dp[length-one]
        dp[length] %= mod
    return sum(dp[low:high+1]) % mod
''','O(high)','O(high)','1 ≤ low ≤ high; zero and one are positive block lengths.')
C('Dynamic programming / Linear sequences','Decode with local transitions',91,'Intermediate','Useful','A string can be partitioned into valid one- or two-character tokens.','At each endpoint add the one-digit transition if nonzero, and the two-digit transition if between 10 and 26.','A zero cannot decode alone, and a leading zero invalidates a two-digit token.','Map numbers 1 through 26 to letters; count ways to decode a nonempty digit string.', ['226'],3,'''
def solve(s):
    dp = [0]*(len(s)+1); dp[0] = 1
    for i in range(1, len(s)+1):
        if s[i-1] != '0': dp[i] += dp[i-1]
        if i >= 2 and 10 <= int(s[i-2:i]) <= 26: dp[i] += dp[i-2]
    return dp[-1]
''','O(n)','O(n)')
G('Dynamic programming / Knapsack','Compress a selection history into a capacity or target.','Decide whether each item can be used once, repeatedly, or once per group. Loop direction encodes that choice.',['Descending capacities prevent reuse.','Ascending capacities permit reuse.'],'dynamic-programming')
G('Dynamic programming / Knapsack / Zero-one choices','Every item is either selected once or skipped.','Use only the previous item layer, explicitly or by descending capacity updates.',['Parity and total-sum bounds can reject impossible targets.'],'dynamic-programming')
C('Dynamic programming / Knapsack / Zero-one choices','Subset-sum feasibility',416,'Intermediate','Core','Split numbers into two equal-sum groups.','Reach half the total by adding each item at most once. Descending sums preserve the previous layer.','Ascending sums accidentally reuse the same number.','Determine whether positive integers can be split into two subsets with equal sums.',[[1,5,11,5]],True,'''
def solve(nums):
    total = sum(nums)
    if total % 2: return False
    target = total//2; dp = [False]*(target+1); dp[0] = True
    for x in nums:
        for s in range(target, x-1, -1): dp[s] = dp[s] or dp[s-x]
    return dp[target]
''','O(n × sum(nums))','O(sum(nums))')
C('Dynamic programming / Knapsack / Zero-one choices','Signed choices to subset counts',494,'Intermediate','Useful','Assign plus or minus to each value to reach a target.','If positive values sum to P and negatives to N, P+N=total and P−N=target. Count subsets summing to (total+target)/2.','Zeros double the number of choices and must be processed.','Count assignments of + or − to every nonnegative value so the expression equals target.',[[1,1,1,1,1],3],5,'''
def solve(nums, target):
    total = sum(nums)
    if abs(target) > total or (total+target)%2: return 0
    goal = (total+target)//2; dp = [0]*(goal+1); dp[0] = 1
    for x in nums:
        for s in range(goal, x-1, -1): dp[s] += dp[s-x]
    return dp[goal]
''','O(n × sum(nums))','O(sum(nums))')
C('Dynamic programming / Knapsack / Zero-one choices','Multiple resource budgets',474,'Intermediate','Useful','Each item consumes two limited resources.','Use dp[zeroBudget][oneBudget] and descend in both dimensions for each string.','Ascending either dimension can count an item more than once.','Select as many binary strings as possible using at most m zeroes and n ones in total.',[['10','0','1'],1,1],2,'''
def solve(strs, m, n):
    dp = [[0]*(n+1) for _ in range(m+1)]
    for s in strs:
        z, o = s.count('0'), s.count('1')
        for i in range(m, z-1, -1):
            for j in range(n, o-1, -1): dp[i][j] = max(dp[i][j], dp[i-z][j-o]+1)
    return dp[m][n]
''','O(total characters + number of strings × mn)','O(mn)')
G('Dynamic programming / Knapsack / Reusable choices','The same choice may be taken repeatedly.','Choose whether order matters, then align loop nesting with the object being counted.',['Coin-first counts combinations; amount-first counts ordered sequences.'],'dynamic-programming')
C('Dynamic programming / Knapsack / Reusable choices','Unbounded minimum cost',322,'Intermediate','Core','Minimize the number of reusable items reaching a target.','For each amount, try every last coin and take the cheapest reachable predecessor plus one.','Use infinity for unreachable amounts, not zero.','Using unlimited coins of the given positive denominations, return the fewest coins totaling amount, or −1.',[[2,5],11],4,'''
def solve(coins, amount):
    dp = [0]+[float('inf')]*amount
    for value in range(1, amount+1):
        for coin in coins:
            if coin <= value: dp[value] = min(dp[value], dp[value-coin]+1)
    return -1 if dp[amount] == float('inf') else dp[amount]
''','O(amount × coins)','O(amount)')
C('Dynamic programming / Knapsack / Reusable choices','Unordered combination counts',518,'Intermediate','Core','Count multisets of reusable choices.','Process each denomination outside the ascending amount loop. Each combination is created in denomination order exactly once.','Reversing the loops counts permutations.','Count combinations of unlimited distinct positive coin denominations totaling amount. Order of coins does not matter.',[5,[1,2,5]],4,'''
def solve(amount, coins):
    dp = [0]*(amount+1); dp[0] = 1
    for coin in coins:
        for value in range(coin, amount+1): dp[value] += dp[value-coin]
    return dp[amount]
''','O(amount × coins)','O(amount)')
C('Dynamic programming / Knapsack / Reusable choices','Ordered composition counts',377,'Intermediate','Useful','Count ordered sequences of reusable choices.','Process target amounts outside; each transition selects the final element of a sequence.','All numbers must be positive for this finite recurrence.','Count ordered sequences of distinct positive candidate numbers that sum to target. Numbers can repeat.',[[1,3],4],3,'''
def solve(nums, target):
    dp = [0]*(target+1); dp[0] = 1
    for total in range(1, target+1):
        for x in nums:
            if x <= total: dp[total] += dp[total-x]
    return dp[target]
''','O(target × n)','O(target)')
G('Dynamic programming / Grids & multiple sequences','Use coordinates or pairs of prefix lengths as state.','A state summarizes the best outcome for prefixes or positions, with transitions to neighboring smaller states.',['Pad boundaries to simplify base cases.','Check whether diagonal state is from the previous row.'],'dynamic-programming')
C('Dynamic programming / Grids & multiple sequences','Grid path accumulation',64,'Foundation','Core','Paths move only right or down.','Each cell takes its value plus the cheaper of its top and left predecessors.','Initialize the top-left cell separately from unreachable boundaries.','Find the minimum sum along a path from top-left to bottom-right in a nonnegative grid, moving right or down.',[[[1,3,1],[1,5,1],[4,2,1]]],7,'''
def solve(grid):
    n = len(grid[0]); dp = [float('inf')]*n; dp[0] = 0
    for row in grid:
        for c, x in enumerate(row): dp[c] = x+min(dp[c], dp[c-1] if c else float('inf'))
    return dp[-1]
''','O(mn)','O(n)')
C('Dynamic programming / Grids & multiple sequences','Longest common subsequence',1143,'Intermediate','Core','Align two sequences while allowing skipped elements.','Equal final characters extend the diagonal; otherwise skip a character from either prefix and take the better result.','Subsequence permits gaps; substring does not.','Return the length of the longest sequence appearing in order, not necessarily contiguously, in both strings.', ['abcde','ace'],3,'''
def solve(a, b):
    dp = [0]*(len(b)+1)
    for x in a:
        prev = dp[:]
        for j, y in enumerate(b, 1):
            dp[j] = prev[j-1]+1 if x == y else max(prev[j], dp[j-1])
    return dp[-1]
''','O(mn)','O(n)')
C('Dynamic programming / Grids & multiple sequences','Edit distance',72,'Intermediate','Core','Transform one string using insertion, deletion, or replacement.','dp[i][j] is the minimum cost for two prefixes. Match for free or pay one for one of three predecessor operations.','Empty prefixes require their length in insertions or deletions.','Return the fewest single-character inserts, deletes, and replacements needed to transform word1 into word2.', ['cat','cut'],1,'''
def solve(a, b):
    dp = list(range(len(b)+1))
    for i, x in enumerate(a, 1):
        prev = dp; dp = [i]+[0]*len(b)
        for j, y in enumerate(b, 1):
            dp[j] = prev[j-1] if x == y else 1+min(prev[j], dp[j-1], prev[j-1])
    return dp[-1]
''','O(mn)','O(n)')
C('Dynamic programming / Grids & multiple sequences','Count matching subsequences',115,'Advanced','Useful','Count how many subsequences of a source equal a target.','For a matching character, add the number of ways to form the preceding target prefix. Update target indices backwards.','The empty target has one match; forward updates reuse a source character.','Count distinct selections of indices from s whose characters spell t.', ['babgbag','bag'],5,'''
def solve(s, t):
    dp = [1]+[0]*len(t)
    for ch in s:
        for j in range(len(t), 0, -1):
            if ch == t[j-1]: dp[j] += dp[j-1]
    return dp[-1]
''','O(mn)','O(n)')
C('Dynamic programming / Grids & multiple sequences','Maximal square ending at a cell',221,'Intermediate','Useful','A filled square must extend three neighboring squares.','For a one cell, its largest square side is one plus the minimum of top, left, and diagonal sides.','Return area rather than side length.','Return the area of the largest square containing only "1" cells in a binary string matrix.',[[['1','1'],['1','1']]],4,'''
def solve(matrix):
    n = len(matrix[0]); dp = [0]*(n+1); best = 0
    for row in matrix:
        diagonal = 0
        for j in range(1, n+1):
            old = dp[j]
            dp[j] = 1+min(dp[j], dp[j-1], diagonal) if row[j-1] == '1' else 0
            best = max(best, dp[j]); diagonal = old
    return best*best
''','O(mn)','O(n)')
G('Dynamic programming / Subsequences','Choose earlier compatible items rather than adjacent items.','Store the best sequence ending at each position; exploit sorted summaries when possible.',['Strict and non-strict comparisons represent different problems.'],'dynamic-programming')
C('Dynamic programming / Subsequences','LIS with minimal tails',300,'Intermediate','Core','Find a longest strictly increasing subsequence.','tails[length−1] is the smallest possible ending value for that length. Replace the first tail at least as large as x.','The tails array is a summary and need not itself be a valid subsequence.','Return the maximum length of a strictly increasing subsequence.',[[4,1,5,2,6]],3,'''
def solve(nums):
    from bisect import bisect_left
    tails = []
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails): tails.append(x)
        else: tails[i] = x
    return len(tails)
''','O(n log n)','O(n)')
C('Dynamic programming / Subsequences','Sort one dimension, reverse ties',354,'Advanced','Useful','Find a chain with both dimensions strictly increasing.','Sort widths ascending but heights descending for equal widths; then LIS on heights cannot take equal-width pairs.','Sorting ties ascending incorrectly permits nesting equal widths.','Find the largest number of envelopes that nest with both width and height strictly increasing. Rotation is not allowed.',[[[5,4],[6,4],[6,7],[2,3]]],3,'''
def solve(envelopes):
    from bisect import bisect_left
    tails = []
    for w, h in sorted(envelopes, key=lambda x:(x[0], -x[1])):
        i = bisect_left(tails, h)
        if i == len(tails): tails.append(h)
        else: tails[i] = h
    return len(tails)
''','O(n log n)','O(n)')
C('Dynamic programming / Subsequences','Count optimal subsequences',673,'Intermediate','Useful','Count how many subsequences attain the best length.','Maintain both best length and its count at each endpoint. Replace count on improvement; add count on an equal-length tie.','Count index selections, including equal-valued alternatives.','Return the number of longest strictly increasing subsequences, distinguished by their index selections.',[[1,3,5,4,7]],2,'''
def solve(nums):
    n = len(nums); length = [1]*n; count = [1]*n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j]+1 > length[i]: length[i], count[i] = length[j]+1, count[j]
                elif length[j]+1 == length[i]: count[i] += count[j]
    best = max(length)
    return sum(count[i] for i in range(n) if length[i] == best)
''','O(n²)','O(n)')
G('Dynamic programming / State machines','A small status controls which actions are legal next.','Represent each legal status explicitly and compute the next layer from old states.',['Avoid same-step transitions that violate the rules.'],'dynamic-programming')
C('Dynamic programming / State machines','Hold and cash states',714,'Intermediate','Core','Trading actions alternate and charge a fee.','Track best profit while holding one share and while holding none; buying and selling connect the states.','Charge the fee once per completed trade.','With unlimited nonoverlapping stock trades and a fee per sale, return maximum profit.',[[1,3,2,8,4,9],2],8,'''
def solve(prices, fee):
    cash, hold = 0, -prices[0]
    for price in prices[1:]: cash, hold = max(cash, hold+price-fee), max(hold, cash-price)
    return cash
''','O(n)','O(n) due to slice; O(1) with index iteration')
C('Dynamic programming / State machines','Cooldown state',309,'Intermediate','Useful','A sale forces a day of inactivity before another purchase.','Separate holding, just-sold, and resting states; buying is allowed only from the old resting state.','Buying directly from just-sold would skip the cooldown.','Trade a stock any number of times, holding at most one share. After a sale, wait one day before buying. Return maximum profit.',[[1,2,3,0,2]],3,'''
def solve(prices):
    hold, sold, rest = float('-inf'), float('-inf'), 0
    for price in prices:
        hold, sold, rest = max(hold, rest-price), hold+price, max(rest, sold)
    return max(rest, sold)
''','O(n)','O(1)')
G('Dynamic programming / Partitions & intervals','Choose where a segment ends or which event happens last.','Use prefix boundaries for partitioning and two endpoints for interval subproblems.',['Choose a last operation when earlier choices change adjacency.'],'dynamic-programming')
C('Dynamic programming / Partitions & intervals','Prefix segmentation',139,'Intermediate','Core','Break a string into permitted dictionary words.','Reachable prefix endpoints form a DAG. A word extends a reachable endpoint to a later endpoint.','A greedy longest word can strand the remaining suffix.','Determine whether s can be segmented into one or more dictionary words. Words may be reused.', ['applepenapple',['apple','pen']],True,'''
def solve(s, wordDict):
    words = set(wordDict); dp = [True]+[False]*len(s)
    lengths = {len(w) for w in words}
    for i in range(1, len(s)+1):
        dp[i] = any(i >= k and dp[i-k] and s[i-k:i] in words for k in lengths)
    return dp[-1]
''','O(n × number of lengths × maximum word length)','O(n + dictionary size)')
C('Dynamic programming / Partitions & intervals','Palindrome interval recurrence',516,'Intermediate','Core','Match two ends of a subsequence inside an interval.','Equal endpoints contribute two plus the interior; otherwise discard one endpoint and take the better result.','Single-character intervals have value one.','Return the length of the longest palindromic subsequence of a nonempty string.', ['bbbab'],4,'''
def solve(s):
    n = len(s); dp = [[0]*n for _ in range(n)]
    for i in range(n-1, -1, -1):
        dp[i][i] = 1
        for j in range(i+1, n):
            dp[i][j] = 2+dp[i+1][j-1] if s[i] == s[j] else max(dp[i+1][j], dp[i][j-1])
    return dp[0][-1]
''','O(n²)','O(n²)')
C('Dynamic programming / Partitions & intervals','Choose the last operation',312,'Advanced','Core','Removing an item changes which neighbors interact.','Choose the last balloon burst inside an interval. Its two outside neighbors are then fixed, separating the left and right subproblems.','Choosing the first balloon does not split into independent intervals.','Burst balloons in any order. Each burst earns the product of its value and its current neighbors, with outside values 1. Maximize coins.',[[3,1,5,8]],167,'''
def solve(nums):
    a = [1]+nums+[1]; n = len(a); dp = [[0]*n for _ in range(n)]
    for width in range(2, n):
        for left in range(n-width):
            right = left+width
            dp[left][right] = max(dp[left][k]+dp[k][right]+a[left]*a[k]*a[right] for k in range(left+1, right))
    return dp[0][-1]
''','O(n³)','O(n²)')
C('Dynamic programming / Partitions & intervals','Weighted interval scheduling',1235,'Advanced','Useful','Choose compatible intervals with unequal rewards.','Sort by ending time. Binary search the last compatible job and compare taking the current job to skipping it.','A job ending exactly when another starts is compatible.','Choose nonoverlapping jobs with startTime, endTime, and profit arrays to maximize total profit.',[[1,2,3,3],[3,4,5,6],[50,10,40,70]],120,'''
def solve(startTime, endTime, profit):
    from bisect import bisect_right
    jobs = sorted(zip(endTime, startTime, profit)); ends = [j[0] for j in jobs]; dp = [0]
    for i, (end, start, value) in enumerate(jobs):
        compatible = bisect_right(ends, start, 0, i)
        dp.append(max(dp[-1], dp[compatible]+value))
    return dp[-1]
''','O(n log n)','O(n)')
G('Dynamic programming / Compressed & advanced states','Use a compact representation when ordinary prefix state is insufficient.','Identify the smallest set, boundary, or arithmetic status that makes future choices independent of history.',['Calculate the state-space size before coding.','Small n may permit exponential states.'],'dynamic-programming','Advanced','Useful')
C('Dynamic programming / Compressed & advanced states','Subset bitmask assignment',526,'Advanced','Useful','Assign distinct values to positions under compatibility rules.','A used-value bitmask determines the next position. Try each unused compatible value and memoize the mask.','Position is popcount(mask)+1, so it need not be a separate state.','Count permutations of 1..n where each value divides its one-based position or the position divides the value.',[3],3,'''
def solve(n):
    from functools import cache
    @cache
    def dfs(mask):
        position = mask.bit_count()+1
        if position > n: return 1
        return sum(dfs(mask | (1 << (x-1))) for x in range(1, n+1)
                   if not mask & (1 << (x-1)) and (x % position == 0 or position % x == 0))
    return dfs(0)
''','O(n 2ⁿ)','O(2ⁿ)','1 ≤ n ≤ 15.')
C('Dynamic programming / Compressed & advanced states','Digit DP with tight bound',233,'Advanced','Specialist','Count a digit across all numbers up to a large bound.','Memoize position and whether the prefix is still tight. Return both the number of completions and their total count of ones.','Leading zeroes are harmless for counting ones, but require a started flag when counting zero digits.','Count all occurrences of digit 1 in decimal representations of integers from 0 through n.',[13],6,'''
def solve(n):
    from functools import cache
    digits = list(map(int, str(n)))
    @cache
    def dp(i, tight):
        if i == len(digits): return (1, 0)
        ways = ones = 0; limit = digits[i] if tight else 9
        for d in range(limit+1):
            count, total = dp(i+1, tight and d == limit)
            ways += count; ones += total + (count if d == 1 else 0)
        return ways, ones
    return dp(0, True)[1]
''','O(number of digits × 10)','O(number of digits)')
C('Dynamic programming / Compressed & advanced states','Game DP as score difference',486,'Intermediate','Useful','Two optimal players alternate choosing from either end.','Define the best score advantage for the player whose turn it is. Taking x yields x minus the opponent’s best remaining advantage.','The recurrence changes perspective each turn.','Two players take either endpoint of nums and add it to their score. Determine whether the first player can finish with at least a tie under optimal play.',[[1,5,2]],False,'''
def solve(nums):
    from functools import cache
    @cache
    def best(left, right):
        if left == right: return nums[left]
        return max(nums[left]-best(left+1, right), nums[right]-best(left, right-1))
    return best(0, len(nums)-1) >= 0
''','O(n²)','O(n²)')
C('Dynamic programming / Compressed & advanced states','Probability propagation',688,'Advanced','Useful','Repeated random moves distribute probability over states.','Keep probability mass at each board cell; divide it equally among eight moves and discard mass leaving the board.','Invalid moves retain their share of the denominator; do not renormalize.','A knight starts at (row,column) on an n×n board and makes k uniformly random knight moves. Return the probability it never leaves the board.',[3,2,0,0],0.0625,'''
def solve(n, k, row, column):
    moves = [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]
    dp = {(row, column): 1.0}
    for _ in range(k):
        nxt = {}
        for (r,c), probability in dp.items():
            for dr, dc in moves:
                a, b = r+dr, c+dc
                if 0 <= a < n and 0 <= b < n: nxt[a,b] = nxt.get((a,b),0)+probability/8
        dp = nxt
    return sum(dp.values())
''','O(kn²)','O(n²)')
C('Dynamic programming / Compressed & advanced states','Monotone deque optimized DP',1696,'Advanced','Useful','Each state needs the maximum among the previous k states.','Keep candidate dp values in decreasing order in a deque, expiring indices outside the jump window.','Expire before reading the best predecessor.','Starting at index 0, jump forward by 1..k positions until the last index. Maximize the sum of visited values.',[[1,-1,-2,4,-7,3],2],7,'''
def solve(nums, k):
    from collections import deque
    q = deque([(0, nums[0])]); best = nums[0]
    for i in range(1, len(nums)):
        while q[0][0] < i-k: q.popleft()
        best = nums[i]+q[0][1]
        while q and q[-1][1] <= best: q.pop()
        q.append((i,best))
    return best
''','O(n)','O(k)')
C('Dynamic programming / Compressed & advanced states','Profile tiling states',790,'Advanced','Specialist','Tiling a narrow board leaves only a few boundary shapes.','Track complete tilings and one-sided gaps; eliminate gap states to derive full[n]=2·full[n−1]+full[n−3].','The recurrence starts at width three; set widths zero, one, and two explicitly.','Count ways to tile a 2×n board with dominoes and L-shaped trominoes, allowing rotations, modulo 1,000,000,007.',[3],5,'''
def solve(n):
    if n <= 2: return [1,1,2][n]
    a, b, c = 1, 1, 2
    for _ in range(3, n+1): a, b, c = b, c, (2*c+a)%1_000_000_007
    return c
''','O(n)','O(1)')

C('Dynamic programming / Compressed & advanced states','Remainder-class maximum',1262,'Intermediate','Useful','Only a sum modulo a small divisor affects whether the final answer is valid.','After each value, keep the largest achievable sum for each remainder. Read exclusively from the previous layer so an item is used once.','An unreachable remainder must remain negative infinity, including when values are zero.','Choose a subset of nonnegative integers with maximum sum divisible by three.',[[3,6,5,1,8]],18,'''
def solve(nums):
    dp = [0, float('-inf'), float('-inf')]
    for x in nums:
        nxt = dp[:]
        for remainder, value in enumerate(dp):
            candidate = (remainder+x)%3
            nxt[candidate] = max(nxt[candidate], value+x)
        dp = nxt
    return dp[0]
''','O(n)','O(1)')
C('Dynamic programming / Grids & multiple sequences','Blocked-cell path counts',63,'Foundation','Core','Some grid cells cannot belong to any path.','A free cell receives paths from above and left; an obstacle resets its count to zero. Seed the first cell with one path only if free.','Leaving a stale count under an obstacle permits paths to cross it.','Count paths from the top-left to bottom-right of a grid with obstacles marked 1, moving only right or down.',[[[0,0,0],[0,1,0],[0,0,0]]],2,'''
def solve(obstacleGrid):
    dp = [0]*len(obstacleGrid[0])
    dp[0] = int(obstacleGrid[0][0] == 0)
    for row in obstacleGrid:
        for c, blocked in enumerate(row):
            if blocked: dp[c] = 0
            elif c: dp[c] += dp[c-1]
    return dp[-1]
''','O(mn)','O(n)')
C('Dynamic programming / Grids & multiple sequences','Matching suffix lengths',718,'Intermediate','Useful','The match must be contiguous in both sequences.','Let dp[i][j] be the equal suffix length ending at both positions; on a mismatch reset it to zero. Retain the maximum over all endpoints.','Taking the maximum of top and left would solve a subsequence problem instead.','Return the longest length of a contiguous subarray appearing in both integer arrays.',[[1,2,3,2,1],[3,2,1,4,7]],3,'''
def solve(nums1, nums2):
    dp = [0]*(len(nums2)+1); best = 0
    for x in nums1:
        for j in range(len(nums2), 0, -1):
            dp[j] = dp[j-1]+1 if x == nums2[j-1] else 0
            best = max(best, dp[j])
    return best
''','O(mn)','O(n)')
C('Dynamic programming / Subsequences','Reconstruct a compatible chain',368,'Intermediate','Useful','The actual chain is required, rather than just its length.','Sort positive values; store the length and predecessor index of the best divisible chain ending at each value, then backtrack from the best endpoint.','Sorting makes divisibility transitive along the recovered chain.','Return any largest subset of distinct positive integers in which every pair has one value dividing the other.',[[1,2,4,8]],[1,2,4,8],'''
def solve(nums):
    nums = sorted(nums); n = len(nums)
    length = [1]*n; parent = [-1]*n
    for i in range(n):
        for j in range(i):
            if nums[i]%nums[j] == 0 and length[j]+1 > length[i]:
                length[i], parent[i] = length[j]+1, j
    if not n: return []
    i = max(range(n), key=lambda x: length[x]); answer = []
    while i != -1:
        answer.append(nums[i]); i = parent[i]
    return answer[::-1]
''','O(n²)','O(n)')
C('Dynamic programming / State machines','Bounded transaction layers',188,'Advanced','Useful','A trade limit makes the number of completed sells part of the state.','For each allowed trade, update cash and hold from the previous day. A sale consumes one transaction; a purchase does not.','Updating from fresh states can incorrectly buy and sell on the same day.','With at most k nonoverlapping stock transactions, maximize profit from daily prices.',[2,[2,4,1]],2,'''
def solve(k, prices):
    if not prices or not k: return 0
    if k >= len(prices)//2:
        return sum(max(0, prices[i]-prices[i-1]) for i in range(1,len(prices)))
    cash = [0]+[float('-inf')]*k
    hold = [float('-inf')]*(k+1)
    for price in prices:
        next_cash, next_hold = cash[:], hold[:]
        for used in range(k+1):
            next_hold[used] = max(hold[used], cash[used]-price)
            if used: next_cash[used] = max(cash[used], hold[used-1]+price)
        cash, hold = next_cash, next_hold
    return max(cash)
''','O(nk)','O(k)')
