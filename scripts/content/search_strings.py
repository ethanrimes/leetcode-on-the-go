from .base import category as G, card as C

G('Backtracking & enumeration','Explore a decision tree while pruning choices that cannot lead to a valid result.','Choose, recurse, and undo. Define whether order matters and whether values may repeat before designing the branches.',['Copy a completed path before storing it.','Separate branch-level deduplication from global visited state.'],'backtracking')
G('Backtracking & enumeration / Choice trees','Enumerate subsets, permutations, and combinations with deliberate branch ordering.','Use a start index for combinations and a used set for permutations.',['Sorting enables duplicate skipping and bound pruning.'],'backtracking')
C('Backtracking & enumeration / Choice trees','Subsets: include or exclude',78,'Foundation','Core','Every item independently belongs or does not belong to a result.','At each position, recurse once without the item and once with it.','Store a copy, since later backtracking mutates the same path.','Return all subsets of distinct input values, including the empty subset. Result order is irrelevant.',[[1,2]],[[],[2],[1],[1,2]],'''
def solve(nums):
    out=[]; path=[]
    def dfs(i):
        if i==len(nums): out.append(path[:]); return
        dfs(i+1)
        path.append(nums[i]); dfs(i+1); path.pop()
    dfs(0)
    return out
''','O(n 2ⁿ)','O(n) auxiliary, O(n 2ⁿ) output')
C('Backtracking & enumeration / Choice trees','Permutations with a used set',46,'Foundation','Core','Fill ordered positions with distinct choices.','At each position try every unused index, then release it after recursion.','A start index would exclude valid permutations.','Return every ordering of distinct values. Result order is irrelevant.',[[1,2]],[[1,2],[2,1]],'''
def solve(nums):
    out=[]; path=[]; used=[False]*len(nums)
    def dfs():
        if len(path)==len(nums): out.append(path[:]); return
        for i,x in enumerate(nums):
            if not used[i]:
                used[i]=True; path.append(x); dfs(); path.pop(); used[i]=False
    dfs()
    return out
''','O(n × n!)','O(n) auxiliary')
C('Backtracking & enumeration / Choice trees','Duplicate-aware combinations',40,'Intermediate','Core','Equal-valued items must not produce duplicate results.','Sort the input; skip equal siblings at the same depth, while allowing equal values at different depths when separate copies exist.','Skip only when i>start, not whenever i>0.','Return unique combinations of positive candidates summing to target. Each input position may be used at most once.',[[1,1,2,5],3],[[1,2]],'''
def solve(candidates,target):
    a=sorted(candidates); out=[]; path=[]
    def dfs(start,remaining):
        if remaining==0: out.append(path[:]); return
        for i in range(start,len(a)):
            if i>start and a[i]==a[i-1]: continue
            if a[i]>remaining: break
            path.append(a[i]); dfs(i+1,remaining-a[i]); path.pop()
    dfs(0,target)
    return out
''','O(n 2ⁿ) upper bound','O(n) auxiliary')
C('Backtracking & enumeration / Choice trees','Reusable combinations',39,'Intermediate','Core','A choice may be repeated but combination order should not matter.','Use nondecreasing candidate indices and recurse with the same index after selecting a value.','Recurse with i+1 only when reuse is forbidden.','Return combinations of distinct positive candidate values summing to target. Each value may be used any number of times.',[[2,3,5],8],[[2,2,2,2],[2,3,3],[3,5]],'''
def solve(candidates,target):
    a=sorted(candidates); out=[]; path=[]
    def dfs(start,left):
        if left==0: out.append(path[:]); return
        for i in range(start,len(a)):
            if a[i]>left: break
            path.append(a[i]); dfs(i,left-a[i]); path.pop()
    dfs(0,target)
    return out
''','Exponential in target/min(candidates)','O(target/min(candidates)) auxiliary')
C('Backtracking & enumeration / Choice trees','Prefix-valid generation',22,'Intermediate','Core','Generate only prefixes that can still become valid.','Add an opener while fewer than n are used; add a closer only when closers are fewer than openers.','Filtering all 2^(2n) strings after generation does unnecessary work.','Generate every balanced string containing n pairs of parentheses.',[2],['(())','()()'],'''
def solve(n):
    out=[]
    def dfs(s,opened,closed):
        if closed==n: out.append(s); return
        if opened<n: dfs(s+'(',opened+1,closed)
        if closed<opened: dfs(s+')',opened,closed+1)
    dfs('',0,0)
    return out
''','O(n × Catalan(n))','O(n²) recursion strings, excluding output')
G('Backtracking & enumeration / Constraint search','Reject partial assignments as soon as they violate a constraint.','Maintain fast occupancy tests and restore all changed state when leaving a branch.',['A visited set for one path must be undone before another path.'],'backtracking')
C('Backtracking & enumeration / Constraint search','Grid path backtracking',79,'Intermediate','Core','A path spells a word without reusing cells.','Try each starting cell; mark a cell while exploring its neighbors and unmark it on return.','Different candidate paths may reuse a cell, but one path may not.','Determine whether word can be spelled by orthogonally adjacent grid cells with no cell reused within the path.',[[['A','B'],['C','D']],'ABD'],True,'''
def solve(board,word):
    m,n=len(board),len(board[0]); used=set()
    def dfs(r,c,i):
        if i==len(word): return True
        if not(0<=r<m and 0<=c<n) or (r,c) in used or board[r][c]!=word[i]: return False
        used.add((r,c))
        found=any(dfs(a,b,i+1) for a,b in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)])
        used.remove((r,c)); return found
    return any(dfs(r,c,0) for r in range(m) for c in range(n))
''','O(mn × 4^wordLength) upper bound','O(wordLength)')
C('Backtracking & enumeration / Constraint search','Column and diagonal occupancy',52,'Advanced','Useful','Place one nonconflicting object per row.','For each row, reject occupied columns and diagonals identified by row−col and row+col.','Diagonal IDs can be negative.','Return the number of ways to place n queens on an n×n board with no shared row, column, or diagonal.',[4],2,'''
def solve(n):
    cols=set(); down=set(); up=set()
    def dfs(row):
        if row==n: return 1
        total=0
        for col in range(n):
            if col in cols or row-col in down or row+col in up: continue
            cols.add(col); down.add(row-col); up.add(row+col)
            total+=dfs(row+1)
            cols.remove(col); down.remove(row-col); up.remove(row+col)
        return total
    return dfs(0)
''','O(n × n!) upper bound','O(n)')
C('Backtracking & enumeration / Constraint search','Meet in the middle',1755,'Advanced','Useful','Subset search is too large for 2ⁿ but manageable at 2^(n/2).','Enumerate sums in each half, sort one side, and binary search the complementary value for each sum from the other half.','Negative values prevent simple target-overflow pruning.','Choose any subsequence, possibly empty, whose sum is closest to goal. Return the minimum absolute difference.',[[5,-7,3,5],6],0,'''
def solve(nums,goal):
    from bisect import bisect_left
    def sums(a):
        out=[0]
        for x in a: out += [v+x for v in out]
        return out
    mid=len(nums)//2; right=sorted(sums(nums[mid:])); best=abs(goal)
    for left in sums(nums[:mid]):
        i=bisect_left(right,goal-left)
        for j in (i-1,i):
            if 0<=j<len(right): best=min(best,abs(left+right[j]-goal))
    return best
''','O(n 2^(n/2))','O(2^(n/2))')

G('Strings & tries','Reuse shared prefixes, suffixes, and symmetry.','Separate exact matching from hashing and choose preprocessing that matches the query workload.',['Hash equality alone is not proof of string equality.','Be explicit about characters versus bytes.'],'string')
G('Strings & tries / Matching & palindrome structure','Avoid restarting work after every mismatch.','Preserve the longest useful prefix or symmetry radius from prior work.',['Boundary conventions matter as much as the recurrence.'],'string-matching')
C('Strings & tries / Matching & palindrome structure','KMP failure links',28,'Intermediate','Core','Search a pattern while reusing matched prefix work.','Build the longest proper prefix-suffix table. On mismatch, fall back through that table rather than restarting the text scan.','After falling back, test the same text character again.','Return the first index where needle appears in haystack, or −1.', ['ababcabc','abc'],2,'''
def solve(haystack,needle):
    if not needle: return 0
    pi=[0]*len(needle); j=0
    for i in range(1,len(needle)):
        while j and needle[i]!=needle[j]: j=pi[j-1]
        if needle[i]==needle[j]: j+=1
        pi[i]=j
    j=0
    for i,ch in enumerate(haystack):
        while j and ch!=needle[j]: j=pi[j-1]
        if ch==needle[j]: j+=1
        if j==len(needle): return i-j+1
    return -1
''','O(n+m)','O(m)')
C('Strings & tries / Matching & palindrome structure','Z-function prefix matches',2223,'Advanced','Useful','Need the shared-prefix length for every suffix.','Maintain the rightmost interval matching a prefix; initialize inside it from mirrored Z values, then extend beyond the boundary.','Z[0] is the full string length for this scoring problem.','Sum the lengths of the longest common prefixes between s and every suffix of s.', ['babab'],9,'''
def solve(s):
    n=len(s); z=[0]*n; left=right=0
    for i in range(1,n):
        if i<=right: z[i]=min(right-i+1,z[i-left])
        while i+z[i]<n and s[z[i]]==s[i+z[i]]: z[i]+=1
        if i+z[i]-1>right: left,right=i,i+z[i]-1
    return n+sum(z)
''','O(n)','O(n)')
C('Strings & tries / Matching & palindrome structure','Expand around centers',5,'Intermediate','Core','A palindrome grows symmetrically from a character or a gap.','Try every odd and even center and expand while both endpoints match.','Even-length palindromes have no single center character.','Return a longest palindromic contiguous substring. If several exist, any is valid.', ['cbbd'],'bb','''
def solve(s):
    start=end=0
    for center in range(len(s)):
        for left,right in [(center,center),(center,center+1)]:
            while left>=0 and right<len(s) and s[left]==s[right]:
                if right-left>end-start: start,end=left,right
                left-=1; right+=1
    return s[start:end+1]
''','O(n²)','O(1) excluding output')
C('Strings & tries / Matching & palindrome structure','Manacher palindrome radii',5,'Advanced','Specialist','Find every palindrome radius in linear time.','Insert separators to unify odd/even centers, reuse the mirrored radius inside the current rightmost palindrome, then expand.','Use sentinels outside the allowed input alphabet.','Return a longest palindromic contiguous substring of a string of letters and digits.', ['cbbd'],'bb','''
def solve(s):
    t='^#'+'#'.join(s)+'#$'; radius=[0]*len(t); center=right=0
    best_center=best_radius=0
    for i in range(1,len(t)-1):
        if i<right: radius[i]=min(right-i,radius[2*center-i])
        while t[i+radius[i]+1]==t[i-radius[i]-1]: radius[i]+=1
        if i+radius[i]>right: center,right=i,i+radius[i]
        if radius[i]>best_radius: best_center,best_radius=i,radius[i]
    start=(best_center-best_radius)//2
    return s[start:start+best_radius]
''','O(n)','O(n)')
C('Strings & tries / Matching & palindrome structure','Rolling hash with collision verification',187,'Intermediate','Useful','Find repeated fixed-length substrings over a tiny alphabet.','Encode A/C/G/T with two bits. Maintain exactly the last 20 bits, so length-ten DNA strings have collision-free encodings.','The mask must remove characters leaving the window.','Return all length-ten DNA substrings appearing at least twice. Output order is irrelevant.', ['AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT'],['AAAAACCCCC','CCCCCAAAAA'],'''
def solve(s):
    codes={'A':0,'C':1,'G':2,'T':3}; seen=set(); repeated=set(); out=[]; value=0
    for i,ch in enumerate(s):
        value=((value<<2)|codes[ch])&((1<<20)-1)
        if i>=9:
            if value in seen and value not in repeated: out.append(s[i-9:i+1]); repeated.add(value)
            seen.add(value)
    return out
''','O(n)','O(min(n,4¹⁰))')
C('Strings & tries / Matching & palindrome structure','Regex state DP',10,'Advanced','Useful','Match a pattern with optional repeated atoms.','Memoize text and pattern positions. For atom*, either skip the atom pair or consume a matching character without advancing the pattern.','The star repeats its preceding atom; it is not a standalone wildcard.','Match the entire string against a pattern where . matches any character and x* matches zero or more copies of x. Pattern syntax is valid.', ['aab','c*a*b'],True,'''
def solve(s,p):
    from functools import cache
    @cache
    def dp(i,j):
        if j==len(p): return i==len(s)
        first=i<len(s) and p[j] in (s[i],'.')
        if j+1<len(p) and p[j+1]=='*': return dp(i,j+2) or (first and dp(i+1,j))
        return first and dp(i+1,j+1)
    return dp(0,0)
''','O(nm)','O(nm)')
G('Strings & tries / Prefix indexes','Share work among queries with common prefixes.','Represent each prefix by a trie node, or preprocess transition positions when the source string is fixed.',['A terminal marker differs from merely having children.'],'trie')
C('Strings & tries / Prefix indexes','Trie exact and prefix lookup',208,'Intermediate','Core','Support repeated word insertion and prefix queries.','Follow one edge per character and mark word endings independently from prefix existence.','The prefix of an inserted word is not necessarily an inserted word.','Simulate insert, search, and startsWith operations. Return booleans for search and startsWith.',[[['insert','apple'],['search','app'],['startsWith','app'],['search','apple']]],[False,True,True],'''
def solve(operations):
    root={}; out=[]
    for op,word in operations:
        node=root
        if op=='insert':
            for ch in word: node=node.setdefault(ch,{})
            node['$']=True
        else:
            for ch in word:
                if ch not in node: node=None; break
                node=node[ch]
            out.append(node is not None and (op=='startsWith' or '$' in node))
    return out
''','O(total characters)','O(total inserted characters)')
C('Strings & tries / Prefix indexes','Bitwise trie for maximum XOR',421,'Advanced','Useful','Choose a value whose bits disagree as early as possible.','Insert binary representations; query from most significant bit downward, preferring the opposite bit whenever it exists.','Greedy decisions are safe because a higher bit dominates all lower bits combined.','Return the maximum XOR of two values in a nonempty array of nonnegative integers.',[[3,10,5,25,2,8]],28,'''
def solve(nums):
    bits=max(1,max(nums).bit_length()); root={}; answer=0
    for x in nums:
        node=root
        for b in range(bits-1,-1,-1): node=node.setdefault((x>>b)&1,{})
    for x in nums:
        node=root; value=0
        for b in range(bits-1,-1,-1):
            bit=(x>>b)&1
            if bit^1 in node: value|=1<<b; node=node[bit^1]
            else: node=node[bit]
        answer=max(answer,value)
    return answer
''','O(n log U)','O(n log U)')
C('Strings & tries / Prefix indexes','Subsequence position index',792,'Intermediate','Useful','Test many words as subsequences of one fixed text.','Store sorted occurrence positions for each character; binary search the next position after the previous match.','Repeated equal words count as separate inputs.','Count words that appear as subsequences of s, preserving character order while allowing gaps.', ['abcde',['a','bb','acd','ace']],3,'''
def solve(s,words):
    from collections import defaultdict
    from bisect import bisect_right
    positions=defaultdict(list)
    for i,ch in enumerate(s): positions[ch].append(i)
    count=0
    for word in words:
        previous=-1
        for ch in word:
            ids=positions[ch]; j=bisect_right(ids,previous)
            if j==len(ids): break
            previous=ids[j]
        else: count+=1
    return count
''','O(|s| + total word characters × log |s|)','O(|s|)')
