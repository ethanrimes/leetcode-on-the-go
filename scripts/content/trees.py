from .base import category as G, card as C, problems

G('Trees & linked lists','Use structural relationships to control traversal and local updates.','On trees, decide whether information flows down from ancestors or up from children. On lists, preserve the next pointer before rewiring.',['A recursive return value should have one precise meaning.','Use a dummy node when the head may change.'],'tree')
G('Trees & linked lists / Binary tree traversal','Traversal order determines when information is available.','Use preorder to carry ancestor state, inorder for BST ordering, and postorder to combine child results.',['Recursion uses O(height) stack space.','Prefer explicit stacks for very deep inputs.'],'binary-tree','Foundation')
C('Trees & linked lists / Binary tree traversal','Postorder subtree aggregation',104,'Foundation','Core','A parent’s result combines child results.','An empty subtree has depth zero; every real node has one plus its deeper child’s depth.','Count nodes along the path, not edges.','Return the maximum number of nodes on a root-to-leaf path. Tree examples use level-order arrays with null for absent children.',[[3,9,20,None,None,15,7]],3,'''
def solve(root):
    if root is None: return 0
    return 1+max(solve(root.left),solve(root.right))
''','O(n)','O(height)')
C('Trees & linked lists / Binary tree traversal','Breadth-first levels',102,'Foundation','Core','Group tree nodes by their distance from the root.','Process exactly the current queue length before beginning the next level.','Reading a growing queue length inside the level loop mixes levels.','Return node values grouped by tree depth, from root to leaves and left to right.',[[3,9,20,None,None,15,7]],[[3],[9,20],[15,7]],'''
def solve(root):
    from collections import deque
    if not root: return []
    q=deque([root]); out=[]
    while q:
        level=[]
        for _ in range(len(q)):
            node=q.popleft(); level.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        out.append(level)
    return out
''','O(n)','O(width) excluding output')
C('Trees & linked lists / Binary tree traversal','Ancestor state with prefix counts',437,'Intermediate','Useful','Count downward paths meeting a sum, starting at any ancestor.','Maintain prefix-sum frequencies only along the current root-to-node path. Remove the current prefix when returning.','Forgetting to backtrack counts creates paths across unrelated branches.','Count downward nonempty paths with sum targetSum. Paths need not start at the root or end at a leaf.',[[10,5,-3,3,2,None,11,3,-2,None,1],8],3,'''
def solve(root, targetSum):
    counts={0:1}
    def dfs(node,total):
        if not node: return 0
        total+=node.val; answer=counts.get(total-targetSum,0)
        counts[total]=counts.get(total,0)+1
        answer+=dfs(node.left,total)+dfs(node.right,total)
        counts[total]-=1
        return answer
    return dfs(root,0)
''','O(n) expected','O(height)')
C('Trees & linked lists / Binary tree traversal','Lowest common ancestor',236,'Intermediate','Core','Find where two target paths first meet.','Return a found target upward; when both children return a target, the current node is the split point.','This version assumes both distinct targets exist and node values are unique.','Given a binary tree with unique values and existing target values p and q, return the value of their lowest common ancestor.',[[3,5,1,6,2,0,8,None,None,7,4],5,1],3,'''
def solve(root, p, q):
    def lca(node):
        if not node or node.val in (p,q): return node
        left,right=lca(node.left),lca(node.right)
        if left and right: return node
        return left or right
    return lca(root).val
''','O(n)','O(height)')
C('Trees & linked lists / Binary tree traversal','BST bounds invariant',98,'Intermediate','Core','Validate a global ordering rule throughout a tree.','Pass an open interval of allowed values to each child, tightening its appropriate bound at the parent.','Comparing only a node with its immediate children misses deeper violations.','Determine whether every node strictly exceeds all values in its left subtree and is strictly smaller than all values in its right subtree.',[[5,1,4,None,None,3,6]],False,'''
def solve(root):
    def valid(node, low, high):
        if not node: return True
        return low < node.val < high and valid(node.left,low,node.val) and valid(node.right,node.val,high)
    return valid(root,float('-inf'),float('inf'))
''','O(n)','O(height)')
C('Trees & linked lists / Binary tree traversal','Iterative inorder selection',230,'Intermediate','Core','Select an ordered value in a binary search tree.','Push the left spine, visit the next smallest node, then traverse its right subtree.','Inorder ordering holds only for a valid BST.','Return the kth smallest node value in a BST, with k starting at 1.',[[3,1,4,None,2],2],2,'''
def solve(root, k):
    stack=[]; node=root
    while stack or node:
        while node: stack.append(node); node=node.left
        node=stack.pop(); k-=1
        if k==0: return node.val
        node=node.right
''','O(height + k)','O(height)')
G('Trees & linked lists / Tree dynamic programming','Return a small summary of each subtree and combine it once.','Separate the value returned to a parent from a complete answer that may use multiple child branches.',['A path passed upward can use only one branch.','Use rerooting when every node needs an answer.'],'dynamic-programming')
C('Trees & linked lists / Tree dynamic programming','Diameter from two best branches',543,'Foundation','Core','The best path passes through some turning node.','Return subtree height while updating the global answer from leftHeight+rightHeight at each node.','The diameter is measured in edges.','Return the largest number of edges on any path between two nodes of a binary tree.',[[1,2,3,4,5]],3,'''
def solve(root):
    answer=0
    def height(node):
        nonlocal answer
        if not node: return 0
        left,right=height(node.left),height(node.right)
        answer=max(answer,left+right)
        return 1+max(left,right)
    height(root)
    return answer
''','O(n)','O(height)')
C('Trees & linked lists / Tree dynamic programming','Maximum path gain',124,'Advanced','Core','A path may turn once, but a parent can extend only one branch.','Clamp negative child gains to zero; evaluate a two-branch path locally and return a one-branch gain upward.','Initialize the answer to −infinity for all-negative trees.','Find the maximum sum of a nonempty simple path in a binary tree.',[[-10,9,20,None,None,15,7]],42,'''
def solve(root):
    answer=float('-inf')
    def gain(node):
        nonlocal answer
        if not node: return 0
        left,right=max(0,gain(node.left)),max(0,gain(node.right))
        answer=max(answer,node.val+left+right)
        return node.val+max(left,right)
    gain(root)
    return answer
''','O(n)','O(height)')
C('Trees & linked lists / Tree dynamic programming','Tree independent set',337,'Intermediate','Core','Selecting a node excludes its direct children.','Return two values: best sum skipping this node and best sum taking it. Taking requires skipping both children.','Grandchildren may be selected when the current node is selected.','Choose nonadjacent tree nodes, with no parent-child pair selected, to maximize their nonnegative values.',[[3,2,3,None,3,None,1]],7,'''
def solve(root):
    def dfs(node):
        if not node: return 0,0
        l0,l1=dfs(node.left); r0,r1=dfs(node.right)
        return max(l0,l1)+max(r0,r1), node.val+l0+r0
    return max(dfs(root))
''','O(n)','O(height)')
C('Trees & linked lists / Tree dynamic programming','Rerooting with subtree sizes',834,'Advanced','Useful','Compute distance sums from every possible tree root.','First collect subtree sizes and root distances. Moving the root across an edge brings size[child] nodes closer and all others farther away.','The reroot transition is answer[child]=answer[parent]+n−2·size[child].','For each vertex of an undirected tree numbered 0..n−1, return the sum of distances to all other vertices.',[3,[[0,1],[1,2]]],[3,2,3],'''
def solve(n, edges):
    graph=[[] for _ in range(n)]
    for a,b in edges: graph[a].append(b); graph[b].append(a)
    parent=[-1]*n; order=[0]
    for u in order:
        for v in graph[u]:
            if v != parent[u]: parent[v]=u; order.append(v)
    size=[1]*n; answer=[0]*n
    for u in reversed(order[1:]):
        size[parent[u]]+=size[u]; answer[parent[u]]+=answer[u]+size[u]
    for u in order[1:]: answer[u]=answer[parent[u]]+n-2*size[u]
    return answer
''','O(n)','O(n)')
C('Trees & linked lists / Tree dynamic programming','Greedy camera states',968,'Advanced','Useful','Cover each tree node by itself or a neighbor.','Return uncovered, camera, or covered status. Place a camera when a child is uncovered, postponing placement toward parents.','After postorder, the root may still be uncovered.','A camera covers a node, its parent, and its children. Return the minimum cameras needed to cover a binary tree.',[[0,0,None,0,0]],1,'''
def solve(root):
    cameras=0
    def state(node):
        nonlocal cameras
        if not node: return 2
        left,right=state(node.left),state(node.right)
        if left==0 or right==0: cameras+=1; return 1
        if left==1 or right==1: return 2
        return 0
    if state(root)==0: cameras+=1
    return cameras
''','O(n)','O(height)')
G('Trees & linked lists / Linked list pointers','Keep track of identity while changing links.','Use a dummy head, a saved next pointer, or a fixed gap between pointers to remove boundary special cases.',['Array examples represent a linked list.','Solutions receive ListNode objects with val and next.'],'linked-list','Foundation')
C('Trees & linked lists / Linked list pointers','Iterative pointer reversal',206,'Foundation','Core','Reverse every next link of a chain.','Save the next node before pointing the current node backward, then advance both pointers.','Overwriting next without saving it loses the remaining list.','Reverse a singly linked list and return its new head. Examples display node values as arrays.',[[1,2,3]],[3,2,1],'''
def solve(head):
    previous=None
    while head:
        nxt=head.next; head.next=previous; previous=head; head=nxt
    return previous
''','O(n)','O(1)')
C('Trees & linked lists / Linked list pointers','Fixed-gap deletion',19,'Intermediate','Core','Remove a node identified from the tail.','Advance a fast pointer n steps from a dummy head, then move both pointers until fast reaches the last node.','A dummy head makes removing the original head a normal case.','Remove the nth node from the end of a singly linked list. n is valid; return the new head.',[[1,2,3,4],2],[1,2,4],'''
def solve(head, n):
    class Dummy:
        def __init__(self, nxt): self.next=nxt
    dummy=Dummy(head); slow=fast=dummy
    for _ in range(n): fast=fast.next
    while fast.next: slow=slow.next; fast=fast.next
    slow.next=slow.next.next
    return dummy.next
''','O(n)','O(1)')
C('Trees & linked lists / Linked list pointers','Floyd cycle meeting',141,'Foundation','Core','Detect a loop with constant memory.','Move one pointer one link and another two links; inside a cycle their relative distance eventually becomes zero.','Compare node identity, not equal values.','Return whether a linked list contains a cycle. Study arguments are [values, pos], where pos is the tail’s next index or −1.',[[3,2,0,-4],1],True,'''
def solve(head):
    slow=fast=head
    while fast and fast.next:
        slow=slow.next; fast=fast.next.next
        if slow is fast: return True
    return False
''','O(n)','O(1)')
C('Trees & linked lists / Linked list pointers','Merge sorted chains',21,'Foundation','Core','Combine two ordered streams by comparing their heads.','Attach the smaller current node to a dummy-headed output and advance that input. Attach the leftover suffix when one ends.','Reuse nodes without losing their next links.','Merge two sorted singly linked lists into one sorted list and return its head.',[[1,3,5],[2,4]],[1,2,3,4,5],'''
def solve(a, b):
    class Dummy:
        def __init__(self): self.next=None
    dummy=tail=Dummy()
    while a and b:
        if a.val <= b.val: tail.next=a; a=a.next
        else: tail.next=b; b=b.next
        tail=tail.next
    tail.next=a or b
    return dummy.next
''','O(m+n)','O(1)')

C('Trees & linked lists / Binary tree traversal','Rightmost node per level',199,'Foundation','Useful','Observe the tree as if only the rightmost node at each depth were visible.','BFS processes a complete level together; the final node removed from that level is the visible one.','Do not read the growing queue length after adding children.','Return the right-side view of a binary tree from top to bottom.',[[1,2,3,None,5,None,4]],[1,3,4],'''
def solve(root):
    from collections import deque
    if not root: return []
    queue = deque([root])
    view = []
    while queue:
        size = len(queue)
        for i in range(size):
            node = queue.popleft()
            if i == size - 1: view.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
    return view
''','O(n)','O(width)')
C('Trees & linked lists / Binary tree traversal','Mirror-pair recursion',101,'Foundation','Useful','Decide whether two subtrees reflect one another.','Compare outer children to each other and inner children to each other, recursively.','Comparing left and right subtrees in the same direction tests equality, not symmetry.','Return whether a binary tree is symmetric around its center.',[[1,2,2,3,4,4,3]],True,'''
def solve(root):
    def mirror(left, right):
        if not left or not right: return left is right
        return (left.val == right.val and
                mirror(left.left, right.right) and
                mirror(left.right, right.left))
    return mirror(root.left, root.right) if root else True
''','O(n)','O(height)')
C('Trees & linked lists / Linked list pointers','Fast-slow midpoint',876,'Foundation','Core','Reach the midpoint without knowing the chain length in advance.','Move slow one link and fast two links; when fast ends, slow is at the middle.','For even length, this convention returns the second middle node.','Return the middle node of a singly linked list; examples show its suffix as values.',[[1,2,3,4,5,6]],[4,5,6],'''
def solve(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
''','O(n)','O(1)')

for number in [104,102,437,236,98,230,543,124,337,968,199,101]:
    problems[str(number)]['test']['adapter']='tree'
    problems[str(number)]['constraints'] += ' Input root is a TreeNode with val, left, and right; examples use level-order arrays. Recursive versions use the call stack.'
for number in [206,19,21,876]: problems[str(number)]['test']['adapter']='linked'
problems['141']['test']['adapter']='cycle'
