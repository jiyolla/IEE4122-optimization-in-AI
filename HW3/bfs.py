from collections import deque
import sys
read = sys.stdin.readline

# graph is given input_bfs.txt
# its format is as follows
# Number of nodes, Number of edges, Initial node
# node1 node2 (representing each edge in the graph)
# ...

# You can run bfs.sh for convenience

n, m, start = map(int, read().split())
v = [[] for _ in range(n + 1)]
for i in range(m):
    v1, v2 = map(int, read().split())
    v[v1].append(v2)
    v[v2].append(v1)
for i in range(n + 1):
    v[i].sort()

visited = [False] * (n+1)
res = []
queue = deque()
queue.append(start)
while queue:
    for _ in range(len(queue)):
        v1 = queue.popleft()
        if not visited[v1]:
            visited[v1] = True
            res.append(str(v1))
            queue += v[v1]
print(" ".join(res))
