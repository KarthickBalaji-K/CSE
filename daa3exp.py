import heapq

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


def kruskal(n, edges):
    edges.sort()
    uf = UnionFind(n)
    mst = []
    cost = 0

    for w, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w
            if len(mst) == n - 1:
                break

    return mst, cost


def prim(n, adj, start=0):
    key = [float('inf')] * n
    parent = [-1] * n
    inMST = [False] * n

    key[start] = 0
    pq = [(0, start)]
    mst = []
    cost = 0

    while pq:
        w, u = heapq.heappop(pq)

        if inMST[u]:
            continue

        inMST[u] = True

        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w

        for v, wt in adj.get(u, []):
            if not inMST[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))

    return mst, cost



n = 6

edges = [
    (4, 0, 1),
    (2, 0, 2),
    (6, 1, 2),
    (5, 1, 3),
    (3, 2, 3),
    (4, 2, 4),
    (7, 3, 4),
    (2, 3, 5),
    (5, 4, 5)
]


print("===== INPUT GRAPH =====")
print("Number of Vertices:", n)
print("Edges (Weight, Vertex1, Vertex2):")
for w, u, v in edges:
    print(f"({w} , {u} , {v})")


adj = {}
for w, u, v in edges:
    adj.setdefault(u, []).append((v, w))
    adj.setdefault(v, []).append((u, w))


k_mst, k_cost = kruskal(n, edges[:])
p_mst, p_cost = prim(n, adj)


print("\n===== KRUSKAL'S MST =====")
for u, v, w in k_mst:
    print(f"Edge ({u} - {v})  Weight = {w}")
print("Total MST Cost =", k_cost)

print("\n===== PRIM'S MST =====")
for u, v, w in p_mst:
    print(f"Edge ({u} - {v})  Weight = {w}")
print("Total MST Cost =", p_cost)
