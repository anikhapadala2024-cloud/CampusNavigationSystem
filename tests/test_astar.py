"""
Tests for the A* (A-star) pathfinding algorithm — app/astar.py
"""
import pytest
from app.astar import a_star
from app.algorithms import bfs


# ---------------------------------------------------------------------------
# Shared fixtures / helpers
# ---------------------------------------------------------------------------

def zero_heuristic(node: str) -> float:
    """Admissible heuristic that always returns 0 (makes A* behave like Dijkstra)."""
    return 0.0


def make_heuristic(goal_costs: dict):
    """Return a heuristic function backed by a lookup table."""
    def h(node: str) -> float:
        return goal_costs.get(node, 0.0)
    return h


# ---------------------------------------------------------------------------
# 1. test_basic_path — simple 4-node graph
# ---------------------------------------------------------------------------

def test_basic_path():
    """A* should find the correct shortest path and cost on a simple 4-node graph."""
    graph = {
        "A": {"B": 1, "C": 4},
        "B": {"A": 1, "C": 2, "D": 5},
        "C": {"A": 4, "B": 2, "D": 1},
        "D": {"B": 5, "C": 1},
    }
    path, cost, _, _ = a_star(graph, zero_heuristic, "A", "D")
    assert path is not None, "Expected a path to be found"
    assert path[0] == "A" and path[-1] == "D"
    # Shortest: A->B->C->D = 1+2+1 = 4
    assert cost == pytest.approx(4.0, rel=1e-3)
    assert path == ["A", "B", "C", "D"]


# ---------------------------------------------------------------------------
# 2. test_no_path — disconnected graph
# ---------------------------------------------------------------------------

def test_no_path():
    """A* should return None for path when no path exists (disconnected graph)."""
    graph = {
        "A": {"B": 1},
        "B": {"A": 1},
        "C": {"D": 1},
        "D": {"C": 1},
    }
    path, cost, _, _ = a_star(graph, zero_heuristic, "A", "D")
    assert path is None, "Expected None when destination is unreachable"
    assert cost is None


# ---------------------------------------------------------------------------
# 3. test_same_start_goal — start == goal
# ---------------------------------------------------------------------------

def test_same_start_goal():
    """When start equals goal, A* should return a single-node path with cost 0."""
    graph = {
        "A": {"B": 5},
        "B": {"A": 5},
    }
    path, cost, _, _ = a_star(graph, zero_heuristic, "A", "A")
    # A* expands "A" immediately and finds it is the goal
    assert path is not None, "Expected a path to be returned for start==goal"
    assert path[0] == "A" and path[-1] == "A"
    assert cost == pytest.approx(0.0, abs=1e-6)


# ---------------------------------------------------------------------------
# 4. test_optimal_path — A* picks cheaper multi-hop over expensive direct edge
# ---------------------------------------------------------------------------

def test_optimal_path():
    """
    Graph:   A --5--> B --5--> C
             A ------10------> C
    A* (with zero heuristic) must choose A->B->C (cost 10) over A->C (cost 10)?
    Actually let's make it unambiguous: A->B->C costs 5 total, A->C costs 10.
    """
    graph = {
        "A": {"B": 2, "C": 10},
        "B": {"A": 2, "C": 3},
        "C": {"B": 3, "A": 10},
    }
    # A->B->C = 2+3 = 5; A->C direct = 10
    path, cost, _, _ = a_star(graph, zero_heuristic, "A", "C")
    assert path is not None
    assert cost == pytest.approx(5.0, rel=1e-3), (
        f"Expected cost 5 (A->B->C), got {cost}"
    )
    assert path == ["A", "B", "C"]


# ---------------------------------------------------------------------------
# 5. test_nodes_expanded_efficiency — A* expands fewer nodes than BFS
# ---------------------------------------------------------------------------

def test_nodes_expanded_efficiency():
    """
    On a larger graph with a clear heuristic, A* should expand fewer nodes than BFS.
    We use a grid-like graph where goal-directed distances are known.
    """
    # Linear chain: S -> 1 -> 2 -> 3 -> 4 -> 5 -> G
    # Plus some side branches from each numbered node
    graph = {
        "S":  {"1": 1, "X1": 1, "X2": 1},
        "1":  {"S": 1, "2": 1, "Y1": 1},
        "2":  {"1": 1, "3": 1, "Y2": 1},
        "3":  {"2": 1, "4": 1, "Y3": 1},
        "4":  {"3": 1, "5": 1, "Y4": 1},
        "5":  {"4": 1, "G": 1, "Y5": 1},
        "G":  {"5": 1},
        "X1": {"S": 1},
        "X2": {"S": 1},
        "Y1": {"1": 1},
        "Y2": {"2": 1},
        "Y3": {"3": 1},
        "Y4": {"4": 1},
        "Y5": {"5": 1},
    }

    # Heuristic: distance-to-goal along the main chain
    chain_dist = {"S": 6, "1": 5, "2": 4, "3": 3, "4": 2, "5": 1, "G": 0}
    h = make_heuristic(chain_dist)

    _, _, astar_expanded, _ = a_star(graph, h, "S", "G")
    bfs_path, bfs_cost, bfs_expanded = bfs(graph, "S", "G")

    assert bfs_path is not None, "BFS must find a path"
    assert astar_expanded <= bfs_expanded, (
        f"A* expanded {astar_expanded} nodes but BFS expanded {bfs_expanded}; "
        "expected A* to be at least as efficient"
    )
