from .base import category as G, card as C

G('Graphs & grids','Model states as vertices and legal transitions as edges.','Pick the traversal from edge costs and the information you need: reachability, ordering, components, or optimal paths.',['Mark visits when enqueuing.','Include every variable that affects future moves in the visited state.'],'graph')
G('Graphs & grids / Traversal & components','Explore connected regions without repeating work.','Use DFS for component structure and BFS for shortest paths with equal edge costs.',['Handle disconnected graphs with an outer loop.'],'depth-first-search')
C('Graphs & grids / Traversal & components','Flood-fill connected components',200,'Foundation','Core','Count separate regions of adjacent cells.','Scan for unvisited land, then flood-fill and mark the entire component once.','Only orthogonal neighbors connect in this problem.','Count groups of "1" cells connected horizontally or vertically in a rectangular grid.',[[['1','1','0'],['0','1','0'],['0','0','1']]],2,'''
def solve(grid):
    m, n = len(grid), len(grid[0]); seen = set(); count = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] != '1' or (r,c) in seen: continue
            count += 1; stack = [(r,c)]; seen.add((r,c))
            while stack:
                x, y = stack.pop()
                for a,b in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
                    if 0 <= a < m and 0 <= b < n and grid[a][b]=='1' and (a,b) not in seen:
                        seen.add((a,b)); stack.append((a,b))
    return count
''','O(mn)','O(mn)')
C('Graphs & grids / Traversal & components','Multi-source BFS',994,'Intermediate','Core','Several sources spread simultaneously at unit speed.','Enqueue all sources at distance zero. The first arrival at a fresh cell is its earliest infection time.','Starting separate BFS runs repeats work and mishandles simultaneity.','Each minute rotten oranges (2) rot orthogonally adjacent fresh oranges (1); 0 is empty. Return minutes until no fresh remain, or −1.',[[[2,1,1],[1,1,0],[0,1,1]]],4,'''
def solve(grid):
    from collections import deque
    m, n = len(grid), len(grid[0]); q = deque(); fresh = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 2: q.append((r,c,0))
            if grid[r][c] == 1: fresh += 1
    time = 0
    while q:
        r,c,time = q.popleft()
        for a,b in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]:
            if 0 <= a < m and 0 <= b < n and grid[a][b] == 1:
                grid[a][b] = 2; fresh -= 1; q.append((a,b,time+1))
    return time if fresh == 0 else -1
''','O(mn)','O(mn)')
C('Graphs & grids / Traversal & components','Reverse reachability',417,'Intermediate','Useful','Find states that can reach two destination regions.','Reverse water flow: start from each ocean boundary and climb to equal or higher cells. Intersect the reachable sets.','Forward search from every cell is unnecessarily expensive.','Water flows to orthogonal cells of no greater height. Return cells that can reach both top/left and bottom/right ocean edges.',[[[1,2],[4,3]]],[[0,1],[1,0],[1,1]],'''
def solve(heights):
    m,n = len(heights),len(heights[0])
    def visit(starts):
        seen = set(starts); stack = list(seen)
        while stack:
            r,c = stack.pop()
            for a,b in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]:
                if 0 <= a < m and 0 <= b < n and (a,b) not in seen and heights[a][b] >= heights[r][c]:
                    seen.add((a,b)); stack.append((a,b))
        return seen
    p = visit([(0,c) for c in range(n)]+[(r,0) for r in range(m)])
    a = visit([(m-1,c) for c in range(n)]+[(r,n-1) for r in range(m)])
    return [list(cell) for cell in sorted(p & a)]
''','O(mn)','O(mn)')
C('Graphs & grids / Traversal & components','Bipartite coloring',785,'Intermediate','Core','Every edge must connect opposite groups.','Assign a start color in each component, then require every neighbor to have the opposite color.','An odd cycle creates a color conflict; disconnected components still need starts.','Given an undirected adjacency list, determine whether vertices can be split into two sets with no edge inside a set.',[[[1,3],[0,2],[1,3],[0,2]]],True,'''
def solve(graph):
    color = {}
    for start in range(len(graph)):
        if start in color: continue
        color[start] = 0; stack = [start]
        while stack:
            u = stack.pop()
            for v in graph[u]:
                if v not in color: color[v] = color[u]^1; stack.append(v)
                elif color[v] == color[u]: return False
    return True
''','O(V+E)','O(V)')
C('Graphs & grids / Traversal & components','Bidirectional BFS',127,'Advanced','Useful','Find a shortest transformation with reversible unit steps.','Expand the smaller frontier from either end until the two searches meet.','Both searches must agree on the definition of one step; include both endpoint words in the answer.','Change one lowercase letter at a time through wordList. Return the number of words in a shortest chain from beginWord to endWord, or 0.', ['hit','cog',['hot','dot','dog','lot','log','cog']],5,'''
def solve(beginWord, endWord, wordList):
    remaining = set(wordList)
    if endWord not in remaining: return 0
    front, back = {beginWord}, {endWord}; distance = 1
    remaining.discard(beginWord); remaining.discard(endWord)
    while front and back:
        if len(front) > len(back): front, back = back, front
        nxt = set()
        for word in front:
            for i in range(len(word)):
                for ch in 'abcdefghijklmnopqrstuvwxyz':
                    candidate = word[:i]+ch+word[i+1:]
                    if candidate in back: return distance+1
                    if candidate in remaining: remaining.remove(candidate); nxt.add(candidate)
        front = nxt; distance += 1
    return 0
''','O(26 × V × wordLength²)','O(V × wordLength)')
G('Graphs & grids / Directed order','Dependencies constrain valid processing order.','Track incoming edges or DFS colors to distinguish unfinished dependencies from completed states.',['A visited boolean alone cannot distinguish an active cycle from a completed branch.'],'topological-sort')
C('Graphs & grids / Directed order','Kahn topological sorting',207,'Intermediate','Core','Tasks require other tasks first.','Process zero-indegree vertices and remove their outgoing edges. A cycle exists if not every vertex can be processed.','Prerequisite [a,b] means an edge from b to a.','Given numCourses and pairs [course,prerequisite], determine whether every course can be completed.',[3,[[1,0],[2,1]]],True,'''
def solve(numCourses, prerequisites):
    from collections import deque
    graph = [[] for _ in range(numCourses)]; degree = [0]*numCourses
    for a,b in prerequisites: graph[b].append(a); degree[a] += 1
    q = deque(i for i in range(numCourses) if degree[i] == 0); count = 0
    while q:
        u = q.popleft(); count += 1
        for v in graph[u]:
            degree[v] -= 1
            if degree[v] == 0: q.append(v)
    return count == numCourses
''','O(V+E)','O(V+E)')
C('Graphs & grids / Directed order','Memoized DFS on a DAG',329,'Advanced','Core','Strictly increasing moves form an implicit acyclic graph.','Cache the longest path starting at each cell; strict increase prevents cycles.','Do not share a global visited flag that blocks alternative incoming paths.','Return the longest strictly increasing path in a matrix using orthogonal moves.',[[[9,9,4],[6,6,8],[2,1,1]]],4,'''
def solve(matrix):
    from functools import cache
    m,n = len(matrix),len(matrix[0])
    @cache
    def dfs(r,c):
        best = 1
        for a,b in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]:
            if 0 <= a < m and 0 <= b < n and matrix[a][b] > matrix[r][c]: best = max(best, 1+dfs(a,b))
        return best
    return max(dfs(r,c) for r in range(m) for c in range(n))
''','O(mn)','O(mn), including recursion','For very deep paths use an iterative topological implementation to avoid Python recursion limits.')
C('Graphs & grids / Directed order','Functional-graph cycle peeling',2360,'Advanced','Useful','Each node has at most one outgoing edge.','Peel indegree-zero vertices first. Every remaining component is a directed cycle; walk and count each cycle once.','A missing edge is −1 and must not be treated as a vertex.','Each edges[i] is the unique destination of i or −1. Return the longest directed cycle length, or −1.',[[3,3,4,2,3]],3,'''
def solve(edges):
    from collections import deque
    n=len(edges); degree=[0]*n
    for v in edges:
        if v != -1: degree[v]+=1
    q=deque(i for i in range(n) if degree[i]==0)
    while q:
        u=q.popleft(); v=edges[u]
        if v != -1:
            degree[v]-=1
            if degree[v]==0: q.append(v)
    best=-1
    for i in range(n):
        if degree[i]:
            count=0; u=i
            while degree[u]: degree[u]=0; count+=1; u=edges[u]
            best=max(best,count)
    return best
''','O(V)','O(V)')
G('Graphs & grids / Shortest paths','Edge costs determine the correct frontier discipline.','Use a queue for unit edges, a deque for 0/1 costs, and a heap for nonnegative general costs.',['Dijkstra does not support negative edge weights.','Path state can include stops, fuel, or collected keys.'],'shortest-path')
C('Graphs & grids / Shortest paths','Dijkstra with stale-entry skipping',743,'Intermediate','Core','Find shortest distances with nonnegative edge weights.','Pop the smallest tentative distance; ignore outdated heap entries and relax outgoing edges.','Marking a vertex final when first enqueued is incorrect.','Directed weighted edges times=[u,v,w] transmit a signal from k. Return when all n vertices numbered 1..n receive it, or −1.',[[[2,1,1],[2,3,1],[3,4,1]],4,2],2,'''
def solve(times, n, k):
    from heapq import heappush, heappop
    graph=[[] for _ in range(n+1)]
    for u,v,w in times: graph[u].append((v,w))
    dist=[float('inf')]*(n+1); dist[k]=0; heap=[(0,k)]
    while heap:
        d,u=heappop(heap)
        if d != dist[u]: continue
        for v,w in graph[u]:
            if d+w < dist[v]: dist[v]=d+w; heappush(heap,(d+w,v))
    answer=max(dist[1:])
    return -1 if answer == float('inf') else answer
''','O((V+E) log(V+E))','O(V+E)')
C('Graphs & grids / Shortest paths','Zero-one BFS',2290,'Advanced','Useful','Each transition costs either zero or one.','Relax zero-cost moves to the front of a deque and one-cost moves to the back.','Track best distances; a simple visited-on-enqueue rule can lock in a worse path.','A binary grid charges one removal when entering an obstacle cell. Return minimum removals from top-left to bottom-right; endpoints are empty.',[[[0,1,1],[1,1,0],[1,1,0]]],2,'''
def solve(grid):
    from collections import deque
    m,n=len(grid),len(grid[0]); dist=[[float('inf')]*n for _ in range(m)]; dist[0][0]=0
    q=deque([(0,0,0)])
    while q:
        d,r,c=q.popleft()
        if d != dist[r][c]: continue
        for a,b in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]:
            if 0 <= a < m and 0 <= b < n:
                w=grid[a][b]
                if d+w < dist[a][b]:
                    dist[a][b]=d+w
                    if w: q.append((d+w,a,b))
                    else: q.appendleft((d,a,b))
    return dist[-1][-1]
''','O(mn)','O(mn)')
C('Graphs & grids / Shortest paths','Bounded-edge Bellman–Ford',787,'Intermediate','Useful','Minimize cost with a limit on how many edges can be used.','Each relaxation layer reads the previous layer only. k stops permits at most k+1 edges.','In-place updates can use too many edges in a single round.','Return the cheapest flight from src to dst using at most k intermediate stops, or −1.',[3,[[0,1,100],[1,2,100],[0,2,500]],0,2,1],200,'''
def solve(n, flights, src, dst, k):
    dist=[float('inf')]*n; dist[src]=0
    for _ in range(k+1):
        nxt=dist[:]
        for u,v,w in flights: nxt[v]=min(nxt[v],dist[u]+w)
        dist=nxt
    return -1 if dist[dst] == float('inf') else dist[dst]
''','O(kE + kV)','O(V)')
C('Graphs & grids / Shortest paths','Floyd–Warshall all-pairs closure',1334,'Intermediate','Useful','Many source/destination distances in a small graph.','Allow intermediate vertices one at a time; update d[i][j] via d[i][k]+d[k][j].','The intermediate-vertex loop must be outermost.','Choose the city with fewest other cities reachable within distanceThreshold in an undirected weighted graph; prefer the largest index on ties.',[4,[[0,1,3],[1,2,1],[1,3,4],[2,3,1]],4],3,'''
def solve(n, edges, distanceThreshold):
    d=[[float('inf')]*n for _ in range(n)]
    for i in range(n): d[i][i]=0
    for u,v,w in edges: d[u][v]=d[v][u]=min(d[u][v],w)
    for k in range(n):
        for i in range(n):
            for j in range(n): d[i][j]=min(d[i][j],d[i][k]+d[k][j])
    return min(range(n),key=lambda i:(sum(i!=j and d[i][j]<=distanceThreshold for j in range(n)),-i))
''','O(V³)','O(V²)')
C('Graphs & grids / Shortest paths','Minimax path relaxation',1631,'Intermediate','Useful','Path cost is its worst edge rather than a sum.','Use Dijkstra with candidate=max(currentCost,edgeCost). This remains monotone along a path.','Do not add edge differences; the objective is the maximum difference.','Move orthogonally through a height grid. Minimize the largest absolute height difference along a path between opposite corners.',[[[1,2,2],[3,8,2],[5,3,5]]],2,'''
def solve(heights):
    from heapq import heappush,heappop
    m,n=len(heights),len(heights[0]); d=[[float('inf')]*n for _ in range(m)]; d[0][0]=0; heap=[(0,0,0)]
    while heap:
        cost,r,c=heappop(heap)
        if cost != d[r][c]: continue
        if (r,c)==(m-1,n-1): return cost
        for a,b in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]:
            if 0 <= a < m and 0 <= b < n:
                value=max(cost,abs(heights[r][c]-heights[a][b]))
                if value < d[a][b]: d[a][b]=value; heappush(heap,(value,a,b))
''','O(mn log(mn))','O(mn)')
G('Graphs & grids / Connectivity & structure','Reason about components, critical edges, and edge-covering walks.','Select an invariant such as representative roots, low-link timestamps, or remaining outgoing edges.',['Connectivity and shortest paths answer different questions.'],'union-find','Advanced')
C('Graphs & grids / Connectivity & structure','Union-find cycle detection',684,'Intermediate','Core','Edges are added to an undirected graph.','An edge creates a cycle exactly when both endpoints already share a representative. Use path compression and union by size.','Union-find does not detect directed cycles this way.','A tree on labels 1..n has one extra edge. Return the last input edge that can be removed to restore a tree.',[[[1,2],[1,3],[2,3]]],[2,3],'''
def solve(edges):
    parent=list(range(len(edges)+1)); size=[1]*len(parent)
    def find(x):
        while x != parent[x]: parent[x]=parent[parent[x]]; x=parent[x]
        return x
    for a,b in edges:
        x,y=find(a),find(b)
        if x==y: return [a,b]
        if size[x]<size[y]: x,y=y,x
        parent[y]=x; size[x]+=size[y]
''','O(E α(V)) amortized','O(V)')
C('Graphs & grids / Connectivity & structure','Minimum spanning tree: Prim',1584,'Intermediate','Core','Connect every point with minimum total edge cost.','Grow one component by repeatedly adding the cheapest edge leaving it; update each outside vertex’s best connection.','An MST minimizes total wiring, not each source-to-vertex distance.','Connect all 2D points using Manhattan-distance edges, minimizing total cost.',[[[0,0],[2,2],[3,10],[5,2],[7,0]]],20,'''
def solve(points):
    n=len(points); best=[float('inf')]*n; best[0]=0; used=[False]*n; total=0
    for _ in range(n):
        u=min((i for i in range(n) if not used[i]),key=lambda i:best[i])
        total+=best[u]; used[u]=True
        for v in range(n):
            if not used[v]: best[v]=min(best[v],abs(points[u][0]-points[v][0])+abs(points[u][1]-points[v][1]))
    return total
''','O(V²)','O(V)')
C('Graphs & grids / Connectivity & structure','Eulerian path: Hierholzer',332,'Advanced','Useful','Use every directed edge exactly once.','Consume outgoing edges with a stack and append dead ends in postorder. Reverse the result to obtain the edge-covering walk.','Vertices may repeat; edges are the resource being consumed.','Use every airline ticket once, starting at JFK, to form the lexicographically smallest itinerary. A valid itinerary is guaranteed.',[[['JFK','SFO'],['JFK','ATL'],['ATL','JFK']]],['JFK','ATL','JFK','SFO'],'''
def solve(tickets):
    from collections import defaultdict
    graph=defaultdict(list)
    for a,b in sorted(tickets,reverse=True): graph[a].append(b)
    stack=['JFK']; route=[]
    while stack:
        if graph[stack[-1]]: stack.append(graph[stack[-1]].pop())
        else: route.append(stack.pop())
    return route[::-1]
''','O(E log E)','O(E)')
C('Graphs & grids / Connectivity & structure','Bridges with low-link values',1192,'Advanced','Specialist','Find edges whose removal disconnects an undirected graph.','DFS timestamps record discovery order; low[u] is the earliest ancestor reachable without the parent edge. A child edge is a bridge when low[child]>tin[parent].','Skip the parent edge by ID, not just by endpoint, to handle parallel edges.','Return all critical connections in a connected undirected graph: edges whose removal disconnects it.',[4,[[0,1],[1,2],[2,0],[1,3]]],[[1,3]],'''
def solve(n, connections):
    graph=[[] for _ in range(n)]
    for i,(u,v) in enumerate(connections): graph[u].append((v,i)); graph[v].append((u,i))
    tin=[-1]*n; low=[0]*n; timer=0; answer=[]
    def dfs(u,parent_edge):
        nonlocal timer
        tin[u]=low[u]=timer; timer+=1
        for v,e in graph[u]:
            if e==parent_edge: continue
            if tin[v]>=0: low[u]=min(low[u],tin[v])
            else:
                dfs(v,e); low[u]=min(low[u],low[v])
                if low[v]>tin[u]: answer.append([u,v])
    for u in range(n):
        if tin[u]<0: dfs(u,-1)
    return answer
''','O(V+E)','O(V+E)','For deep graphs, convert the DFS to an explicit stack to avoid Python recursion limits.')
C('Graphs & grids / Traversal & components','Boundary-first component removal',130,'Intermediate','Core','A region survives exactly when it connects to the board boundary.','Flood-fill boundary O cells as safe, then flip only the unmarked O cells and restore the safe markers.','Diagonal contact does not connect cells in this board.','Capture every O region fully surrounded by X cells in a board, modifying the board in place.',[[['X','X','X','X'],['X','O','O','X'],['X','X','O','X'],['X','O','X','X']]], [['X','X','X','X'],['X','X','X','X'],['X','X','X','X'],['X','O','X','X']],'''
def solve(board):
    from collections import deque
    m, n = len(board), len(board[0]); q = deque()
    for r in range(m):
        for c in (0,n-1):
            if board[r][c] == 'O': board[r][c] = '#'; q.append((r,c))
    for c in range(n):
        for r in (0,m-1):
            if board[r][c] == 'O': board[r][c] = '#'; q.append((r,c))
    while q:
        r,c = q.popleft()
        for a,b in ((r+1,c),(r-1,c),(r,c+1),(r,c-1)):
            if 0 <= a < m and 0 <= b < n and board[a][b] == 'O':
                board[a][b] = '#'; q.append((a,b))
    for r in range(m):
        for c in range(n): board[r][c] = 'O' if board[r][c] == '#' else 'X'
    return board
''','O(mn)','O(mn)')
C('Graphs & grids / Traversal & components','Unit-cost eight-direction BFS',1091,'Foundation','Useful','Every legal grid move has equal cost.','Enqueue an open neighbor once and assign its distance on discovery. Include diagonals because they are valid edges here.','The shortest path length counts cells, so the starting cell has distance one.','Find the shortest clear path from top-left to bottom-right in a binary grid, moving in eight directions; blocked cells are 1.',[[[0,1],[1,0]]],2,'''
def solve(grid):
    from collections import deque
    n = len(grid)
    if grid[0][0] or grid[-1][-1]: return -1
    q = deque([(0,0,1)]); grid[0][0] = 1
    while q:
        r,c,d = q.popleft()
        if r == n-1 and c == n-1: return d
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                a,b = r+dr,c+dc
                if 0 <= a < n and 0 <= b < n and grid[a][b] == 0:
                    grid[a][b] = 1; q.append((a,b,d+1))
    return -1
''','O(n²)','O(n²)')
C('Graphs & grids / Directed order','Construct a topological order',210,'Intermediate','Core','The task asks for a valid ordering, not only whether one exists.','Repeatedly take a zero-indegree course, append it, and release courses depending on it. Return an empty list if a cycle prevents a complete order.','An ordering can vary; any permutation respecting every prerequisite is valid.','Return a possible order of all courses given [course,prerequisite] edges, or [] if impossible.',[3,[[1,0],[2,1]]],[0,1,2],'''
def solve(numCourses, prerequisites):
    from collections import deque
    graph = [[] for _ in range(numCourses)]; degree = [0]*numCourses
    for course, before in prerequisites:
        graph[before].append(course); degree[course] += 1
    q = deque(i for i in range(numCourses) if degree[i] == 0); order = []
    while q:
        u = q.popleft(); order.append(u)
        for v in graph[u]:
            degree[v] -= 1
            if degree[v] == 0: q.append(v)
    return order if len(order) == numCourses else []
''','O(V+E)','O(V+E)')
C('Graphs & grids / Connectivity & structure','Count components with union-find',547,'Intermediate','Useful','An adjacency matrix describes undirected connections, including indirect ones.','Start with one component per city; each successful union across an upper-triangle edge reduces the count by one.','The diagonal and mirrored half contain no new connections.','Given a symmetric matrix where 1 means two cities connect directly, count connected provinces.',[[[1,1,0],[1,1,0],[0,0,1]]],2,'''
def solve(isConnected):
    n = len(isConnected); parent = list(range(n)); size = [1]*n; count = n
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for i in range(n):
        for j in range(i+1,n):
            if not isConnected[i][j]: continue
            a,b = find(i),find(j)
            if a == b: continue
            if size[a] < size[b]: a,b = b,a
            parent[b] = a; size[a] += size[b]; count -= 1
    return count
''','O(n² α(n))','O(n)')
C('Graphs & grids / Shortest paths','Maximum-product path',1514,'Intermediate','Useful','Edge probabilities multiply rather than add along a route.','Prioritize the largest current path probability in a max heap; relax a neighbor when multiplying by an edge improves it.','A zero-probability path cannot improve any state.','Given undirected edges and success probabilities, return the maximum probability of reaching end from start.',[3,[[0,1],[1,2],[0,2]],[0.5,0.5,0.2],0,2],0.25,'''
def solve(n, edges, succProb, start_node, end_node):
    from heapq import heappush, heappop
    graph = [[] for _ in range(n)]
    for (u,v), p in zip(edges,succProb):
        graph[u].append((v,p)); graph[v].append((u,p))
    best = [0.0]*n; best[start_node] = 1.0; heap = [(-1.0,start_node)]
    while heap:
        neg,u = heappop(heap); probability = -neg
        if probability < best[u]: continue
        if u == end_node: return probability
        for v,p in graph[u]:
            candidate = probability*p
            if candidate > best[v]: best[v] = candidate; heappush(heap,(-candidate,v))
    return 0.0
''','O((V+E) log(V+E))','O(V+E)')
