"""
Comparative tests for all search algorithms — app/algorithms.py and app/astar.py

All tests use a small synthetic graph (not the real campus graph) so results
are deterministic and fast.
"""
import pytest
from app.algorithms import dijkstra, bfs, dfs
from app.astar import a_star


# ---------------------------------------------------------------------------
# Shared synthetic graph
# ---------------------------------------------------------------------------
#
#   A --1--> B --2--> D
#   |        |
#   3        4
#   |        |
#   v        v
#   C --1--> D (also reachable from C)
#
# Shortest A->D: A->B->D = 1+2 = 3
# Alternative:   A->C->D = 3+1 = 4
# Alternative:   A->B->C->D = 1+4+1 = 6  (too long)

GRAPH = {
    "A": {"B": 1, "C": 3},
    "B": {"A": 1, "C": 4, "D": 2},
    "C": {"A": 3, "B": 4, "D": 1},
    "D": {"B": 2, "C": 1},
}

START = "A"
GOAL = "D"


def zero_heuristic(node: str) -> float:
    return 0.0


# ---------------------------------------------------------------------------
# 1. test_dijkstra_finds_optimal
# ---------------------------------------------------------------------------

def test_dijkstra_finds_optimal():
    """Dijkstra must return the same optimal cost as A* (with zero heuristic)."""
    dijk_path, dijk_cost, _ = dijkstra(GRAPH, START, GOAL)
    astar_path, astar_cost, _, _ = a_star(GRAPH, zero_heuristic, START, GOAL)

    assert dijk_path is not None, "Dijkstra should find a path"
    assert astar_path is not None, "A* should find a path"

    assert dijk_cost == pytest.approx(astar_cost, rel=1e-3), (
        f"Dijkstra cost {dijk_cost} != A* cost {astar_cost}"
    )
    # Both should find the optimal cost of 3 (A->B->D)
    assert dijk_cost == pytest.approx(3.0, rel=1e-3)


# ---------------------------------------------------------------------------
# 2. test_bfs_finds_path
# ---------------------------------------------------------------------------

def test_bfs_finds_path():
    """BFS must find *a* path (not necessarily cost-optimal) from A to D."""
    path, cost, expanded = bfs(GRAPH, START, GOAL)

    assert path is not None, "BFS should find a path in a connected graph"
    assert len(path) >= 2, "Path must have at least start and goal nodes"
    assert path[0] == START, f"Path must start at {START}"
    assert path[-1] == GOAL, f"Path must end at {GOAL}"

    # Sanity check: every consecutive pair must be a real edge
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        assert v in GRAPH.get(u, {}), f"BFS returned invalid edge {u}->{v}"


# ---------------------------------------------------------------------------
# 3. test_dfs_finds_path
# ---------------------------------------------------------------------------

def test_dfs_finds_path():
    """DFS must find *a* path (not necessarily cost-optimal) from A to D."""
    path, cost, expanded = dfs(GRAPH, START, GOAL)

    assert path is not None, "DFS should find a path in a connected graph"
    assert len(path) >= 2, "Path must have at least start and goal nodes"
    assert path[0] == START, f"Path must start at {START}"
    assert path[-1] == GOAL, f"Path must end at {GOAL}"

    # Sanity check: every consecutive pair must be a real edge
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        assert v in GRAPH.get(u, {}), f"DFS returned invalid edge {u}->{v}"


# ---------------------------------------------------------------------------
# Bonus: BFS / DFS both return None on a disconnected graph
# ---------------------------------------------------------------------------

def test_bfs_no_path_disconnected():
    """BFS returns None when no path exists."""
    disconnected = {
        "X": {"Y": 1},
        "Y": {"X": 1},
        "Z": {},
    }
    path, cost, _ = bfs(disconnected, "X", "Z")
    assert path is None


def test_dfs_no_path_disconnected():
    """DFS returns None when no path exists."""
    disconnected = {
        "X": {"Y": 1},
        "Y": {"X": 1},
        "Z": {},
    }
    path, cost, _ = dfs(disconnected, "X", "Z")
    assert path is None
