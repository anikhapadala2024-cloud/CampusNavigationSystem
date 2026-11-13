from app.landmarks import LANDMARKS
from app.heuristics import haversine
from typing import Dict

_graph_cache = None

def build_campus_graph(landmarks: Dict, max_distance: float = 400.0) -> Dict:
    graph = {node: {} for node in landmarks}
    nodes = list(landmarks.keys())
    for i, a in enumerate(nodes):
        for b in nodes[i+1:]:
            lat1, lon1 = landmarks[a]
            lat2, lon2 = landmarks[b]
            dist = haversine(lat1, lon1, lat2, lon2)
            if dist <= max_distance:
                graph[a][b] = round(dist, 1)
                graph[b][a] = round(dist, 1)
    return graph

def get_campus_graph() -> Dict:
    global _graph_cache
    if _graph_cache is None:
        _graph_cache = build_campus_graph(LANDMARKS)
    return _graph_cache

def get_landmarks() -> Dict:
    return LANDMARKS
