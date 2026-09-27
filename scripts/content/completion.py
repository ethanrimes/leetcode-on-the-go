from .base import card as C, problems

C('Trees & linked lists / Binary tree traversal','Reconstruct from traversal boundaries',105,'Intermediate','Core','A traversal identifies roots while another separates their subtrees.','Preorder supplies the next root; an inorder index map divides the remaining range into left and right subtrees.','Unique values are required for the index map to identify a single split.','Rebuild the unique binary tree from preorder and inorder traversals of distinct values. The example result displays level-order values.',[[3,9,20,15,7],[9,3,15,20,7]],[3,9,20,None,None,15,7],'''
class TreeNode:
    def __init__(self,val,left=None,right=None): self.val=val; self.left=left; self.right=right

def solve(preorder,inorder):
    positions={x:i for i,x in enumerate(inorder)}; cursor=0
    def build(left,right):
        nonlocal cursor
        if left>=right: return None
        value=preorder[cursor]; cursor+=1; mid=positions[value]
        return TreeNode(value,build(left,mid),build(mid+1,right))
    return build(0,len(inorder))
''','O(n)','O(n)')
problems['105']['test']['adapter']='tree-output'
C('Trees & linked lists / Binary tree traversal','Serialization with null markers',297,'Advanced','Core','Preserve enough information to reconstruct both values and shape.','Use preorder with an explicit marker for every absent child; decoding consumes exactly one token per recursive call.','Values alone cannot distinguish different tree shapes.','Serialize a binary tree and deserialize it without losing shape or values. The study wrapper round-trips the tree and returns its preorder serialization.',[[1,2,3,None,None,4,5]],'1,2,#,#,3,4,#,#,5,#,#','''
class TreeNode:
    def __init__(self,val,left=None,right=None): self.val=val; self.left=left; self.right=right

def serialize(root):
    tokens=[]
    def visit(node):
        if node is None: tokens.append('#'); return
        tokens.append(str(node.val)); visit(node.left); visit(node.right)
    visit(root)
    return ','.join(tokens)

def deserialize(text):
    tokens=iter(text.split(','))
    def read():
        token=next(tokens)
        if token=='#': return None
        return TreeNode(int(token),read(),read())
    return read()

def solve(root):
    return serialize(deserialize(serialize(root)))
''','O(n)','O(n)')
problems['297']['test']['adapter']='tree'
C('Trees & linked lists / Linked list pointers','Reverse a fixed-size group',25,'Advanced','Useful','Reverse complete chunks without changing leftover nodes.','Find the kth node before mutating. Reverse links up to the following node, reconnect the group, and advance the group predecessor.','Do not reverse a trailing group shorter than k.','Reverse each consecutive group of k nodes in a singly linked list. Leave a short final group unchanged.',[[1,2,3,4,5],2],[2,1,4,3,5],'''
def solve(head,k):
    class Dummy:
        def __init__(self,nxt): self.next=nxt
    dummy=before=Dummy(head)
    while True:
        kth=before
        for _ in range(k):
            kth=kth.next
            if kth is None: return dummy.next
        after=kth.next; old_first=before.next; previous=after; current=old_first
        while current is not after:
            nxt=current.next; current.next=previous; previous=current; current=nxt
        before.next=kth; before=old_first
''','O(n)','O(1)')
problems['25']['test']['adapter']='linked'
C('Trees & linked lists / Linked list pointers','Midpoint split and half reversal',234,'Foundation','Useful','Compare symmetric linked-list values without an auxiliary array.','Find the end of the first half using slow/fast pointers, reverse the second half, compare, then restore its links.','Restoring the second half avoids surprising the caller with a mutated list.','Determine whether linked-list values form a palindrome, using constant auxiliary space.',[[1,2,2,1]],True,'''
def solve(head):
    if head is None: return True
    slow=fast=head
    while fast.next and fast.next.next: slow=slow.next; fast=fast.next.next
    def reverse(node):
        previous=None
        while node: nxt=node.next; node.next=previous; previous=node; node=nxt
        return previous
    second=reverse(slow.next); a,b=head,second; valid=True
    while b:
        if a.val!=b.val: valid=False
        a=a.next; b=b.next
    slow.next=reverse(second)
    return valid
''','O(n)','O(1)')
problems['234']['test']['adapter']='linked-bool'
C('Backtracking & enumeration / Choice trees','Partition by valid segments',131,'Intermediate','Core','Enumerate all ways to split a sequence into valid pieces.','Choose the next ending boundary, recurse only when the chosen segment is a palindrome, then undo the segment.','Each branch must advance the start index or recursion will not terminate.','Return every partition of s into contiguous palindromic substrings.', ['aab'],[['a','a','b'],['aa','b']],'''
def solve(s):
    out=[]; path=[]
    def dfs(start):
        if start==len(s): out.append(path[:]); return
        for end in range(start+1,len(s)+1):
            part=s[start:end]
            if part==part[::-1]: path.append(part); dfs(end); path.pop()
    dfs(0)
    return out
''','O(n² 2ⁿ) conservative bound with slice checks','O(n) recursion excluding output and slices')
C('Backtracking & enumeration / Constraint search','Minimum-remaining-values Sudoku search',37,'Advanced','Useful','Constraint satisfaction benefits from branching on the most restricted variable.','Track used digits for each row, column, and box. At every step select the empty cell with fewest available candidates, then try and undo each candidate.','An empty candidate set is an immediate contradiction.','Fill a valid 9×9 Sudoku board containing digits "1".."9" and "." blanks. A unique solution exists. Return the solved board for study.',[[list('53467891.'),list('672195348'),list('198342567'),list('859761423'),list('426853791'),list('713924856'),list('961537284'),list('287419635'),list('345286179')]], [list('534678912'),list('672195348'),list('198342567'),list('859761423'),list('426853791'),list('713924856'),list('961537284'),list('287419635'),list('345286179')],'''
def solve(board):
    rows=[set() for _ in range(9)]; cols=[set() for _ in range(9)]; boxes=[set() for _ in range(9)]; empty=[]; digits=set('123456789')
    for r in range(9):
        for c in range(9):
            ch=board[r][c]
            if ch=='.': empty.append((r,c))
            else: rows[r].add(ch); cols[c].add(ch); boxes[r//3*3+c//3].add(ch)
    def choices(cell):
        r,c=cell; return digits-rows[r]-cols[c]-boxes[r//3*3+c//3]
    def dfs(i):
        if i==len(empty): return True
        j=min(range(i,len(empty)),key=lambda j:len(choices(empty[j])))
        empty[i],empty[j]=empty[j],empty[i]; r,c=empty[i]; b=r//3*3+c//3
        for ch in choices((r,c)):
            board[r][c]=ch; rows[r].add(ch); cols[c].add(ch); boxes[b].add(ch)
            if dfs(i+1): return True
            rows[r].remove(ch); cols[c].remove(ch); boxes[b].remove(ch); board[r][c]='.'
        empty[i],empty[j]=empty[j],empty[i]
        return False
    dfs(0)
    return board
''','O(9ᴱ × E) upper bound for E empty cells','O(E + 81)')
C('Two pointers & windows / Opposing & forward pointers','Resolve water from the lower boundary',42,'Advanced','Core','Water at a position is limited by the smaller of two boundary maxima.','Track the highest wall reached from each side. Resolve the side with smaller known maximum, since the opposite side already provides enough containment.','Update the side maximum before adding its water contribution.','Given nonnegative bar heights of width one, return the total trapped rainwater.',[[0,1,0,2,1,0,1,3,2,1,2,1]],6,'''
def solve(height):
    left,right=0,len(height)-1; left_max=right_max=water=0
    while left<=right:
        if left_max<=right_max:
            left_max=max(left_max,height[left]); water+=left_max-height[left]; left+=1
        else:
            right_max=max(right_max,height[right]); water+=right_max-height[right]; right-=1
    return water
''','O(n)','O(1)')
C('Dynamic programming / Grids & multiple sequences','Reconstruct an optimal sequence',1092,'Advanced','Useful','The problem asks for the actual optimum, not just its value.','Build an LCS-length table, then trace back: shared characters are written once; otherwise follow the better predecessor while emitting the skipped character.','Reconstruction tie-breaking can yield different but equally optimal strings.','Return a shortest string containing both str1 and str2 as subsequences. Any shortest answer is valid.', ['abac','cab'],'cabac','''
def solve(a,b):
    m,n=len(a),len(b); dp=[[0]*(n+1) for _ in range(m+1)]
    for i in range(1,m+1):
        for j in range(1,n+1): dp[i][j]=1+dp[i-1][j-1] if a[i-1]==b[j-1] else max(dp[i-1][j],dp[i][j-1])
    i,j=m,n; out=[]
    while i and j:
        if a[i-1]==b[j-1]: out.append(a[i-1]); i-=1; j-=1
        elif dp[i-1][j]>=dp[i][j-1]: out.append(a[i-1]); i-=1
        else: out.append(b[j-1]); j-=1
    return a[:i]+b[:j]+''.join(reversed(out))
''','O(mn)','O(mn)')
C('Greedy & intervals / Interval decisions','Greedy interval covering',1024,'Intermediate','Useful','Cover a target span with as few available intervals as possible.','Among all clips beginning at or before the current covered endpoint, choose the one extending farthest. Repeat from that endpoint.','A gap with no extension makes coverage impossible.','Select the fewest video clips [start,end] whose union covers [0,time]. Clips may be trimmed. Return −1 when coverage is impossible.',[[[0,2],[4,6],[8,10],[1,9],[1,5],[5,9]],10],3,'''
def solve(clips,time):
    clips=sorted(clips); current=cursor=count=0
    while current<time:
        farthest=current
        while cursor<len(clips) and clips[cursor][0]<=current:
            farthest=max(farthest,clips[cursor][1]); cursor+=1
        if farthest==current: return -1
        current=farthest; count+=1
    return count
''','O(n log n)','O(n)')
