import heapq
from typing import Dict, Callable, List, Tuple, Optional

def a_star(
    graph: Dict,
    heuristic_fn: Callable[[str], float],
    start: str,
    goal: str
) -> Tuple[Optional[List[str]], Optional[float], int, List[str]]:
    open_list = []
    heapq.heappush(open_list, (heuristic_fn(start), 0.0, start))
    came_from: Dict[str, str] = {}
    g_cost: Dict[str, float] = {start: 0.0}
    trace: List[str] = []
    nodes_expanded = 0

    while open_list:
        f, g, current = heapq.heappop(open_list)
        nodes_expanded += 1
        trace.append(f"Expanded: {current} | g={g:.1f} | f={f:.1f}")

        if current == goal:
            path = []
            node = current
            while node in came_from:
                path.append(node)
                node = came_from[node]
            path.append(start)
            path.reverse()
            return path, g_cost[goal], nodes_expanded, trace

        for neighbor, cost in graph.get(current, {}).items():
            new_g = g + cost
            if new_g < g_cost.get(neighbor, float('inf')):
                g_cost[neighbor] = new_g
                came_from[neighbor] = current
                f_cost = new_g + heuristic_fn(neighbor)
                heapq.heappush(open_list, (f_cost, new_g, neighbor))

    return None, None, nodes_expanded, trace
