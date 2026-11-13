"""
Tests for the campus graph builder — app/graph.py and app/landmarks.py
"""
import pytest
from collections import deque

from app.graph import get_campus_graph, build_campus_graph
from app.landmarks import LANDMARKS


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def campus_graph():
    return get_campus_graph()


# ---------------------------------------------------------------------------
# 1. test_all_landmarks_in_graph
# ---------------------------------------------------------------------------

def test_all_landmarks_in_graph(campus_graph):
    """Every landmark defined in LANDMARKS must appear as a key in the graph."""
    for landmark in LANDMARKS:
        assert landmark in campus_graph, (
            f"Landmark '{landmark}' is missing from campus_graph"
        )


# ---------------------------------------------------------------------------
# 2. test_edges_bidirectional
# ---------------------------------------------------------------------------

def test_edges_bidirectional(campus_graph):
    """For every directed edge A->B the reverse edge B->A must exist with same weight."""
    for node_a, neighbors in campus_graph.items():
        for node_b, weight in neighbors.items():
            assert node_b in campus_graph, f"Node '{node_b}' not in graph"
            assert node_a in campus_graph[node_b], (
                f"Edge {node_a}->{node_b} exists but reverse {node_b}->{node_a} is missing"
            )
            assert campus_graph[node_b][node_a] == pytest.approx(weight, rel=1e-3), (
                f"Edge {node_a}->{node_b} weight {weight} != "
                f"reverse weight {campus_graph[node_b][node_a]}"
            )


# ---------------------------------------------------------------------------
# 3. test_distances_positive
# ---------------------------------------------------------------------------

def test_distances_positive(campus_graph):
    """All edge weights must be strictly positive (> 0)."""
    for node, neighbors in campus_graph.items():
        for neighbor, weight in neighbors.items():
            assert weight > 0, (
                f"Edge {node}->{neighbor} has non-positive weight {weight}"
            )


# ---------------------------------------------------------------------------
# 4. test_graph_connected — BFS from Main Gate reaches at least 5 other nodes
# ---------------------------------------------------------------------------

def test_graph_connected(campus_graph):
    """BFS from 'Main Gate' must reach at least 5 other distinct nodes."""
    start = "Main Gate"
    assert start in campus_graph, f"'{start}' not found in campus graph"

    visited = set()
    queue = deque([start])
    visited.add(start)

    while queue:
        node = queue.popleft()
        for neighbor in campus_graph.get(node, {}):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    reachable_others = visited - {start}
    assert len(reachable_others) >= 5, (
        f"Expected at least 5 nodes reachable from 'Main Gate', "
        f"but only reached {len(reachable_others)}: {reachable_others}"
    )


# ---------------------------------------------------------------------------
# 5. test_max_distance_respected — no edge exceeds 400 m
# ---------------------------------------------------------------------------

def test_max_distance_respected(campus_graph):
    """No edge in the default campus graph should exceed 400 metres."""
    max_allowed = 400.0
    for node, neighbors in campus_graph.items():
        for neighbor, weight in neighbors.items():
            assert weight <= max_allowed, (
                f"Edge {node}->{neighbor} has weight {weight:.1f} m, "
                f"which exceeds the {max_allowed} m limit"
            )
