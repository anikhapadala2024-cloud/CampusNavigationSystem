import heapq
from collections import deque
from typing import Dict, List, Optional, Tuple

def dijkstra(graph: Dict, start: str, goal: str) -> Tuple[Optional[List[str]], Optional[float], int]:
    pq = [(0.0, start)]
    dist = {start: 0.0}
    came_from: Dict[str, str] = {}
    nodes_expanded = 0
    while pq:
        d, u = heapq.heappop(pq)
        nodes_expanded += 1
        if u == goal:
            path = []
            while u in came_from:
                path.append(u)
                u = came_from[u]
            path.append(start)
            return path[::-1], dist[goal], nodes_expanded
        for v, w in graph.get(u, {}).items():
            nd = d + w
            if nd < dist.get(v, float('inf')):
                dist[v] = nd
                came_from[v] = u
                heapq.heappush(pq, (nd, v))
    return None, None, nodes_expanded

def bfs(graph: Dict, start: str, goal: str) -> Tuple[Optional[List[str]], Optional[int], int]:
    queue = deque([(start, [start])])
    visited = {start}
    nodes_expanded = 0
    while queue:
        node, path = queue.popleft()
        nodes_expanded += 1
        if node == goal:
            return path, len(path) - 1, nodes_expanded
        for neighbor in graph.get(node, {}):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None, None, nodes_expanded

def dfs(graph: Dict, start: str, goal: str) -> Tuple[Optional[List[str]], Optional[float], int]:
    stack = [(start, [start], 0.0)]
    visited = set()
    nodes_expanded = 0
    while stack:
        node, path, cost = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        nodes_expanded += 1
        if node == goal:
            return path, cost, nodes_expanded
        for neighbor, weight in graph.get(node, {}).items():
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor], cost + weight))
    return None, None, nodes_expanded
