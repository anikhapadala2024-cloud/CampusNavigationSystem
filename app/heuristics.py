from math import radians, cos, sin, asin, sqrt
from typing import Callable, Dict, Tuple

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2)**2
    return R * 2 * asin(sqrt(a))

def make_heuristic(goal: str, landmarks: Dict[str, Tuple[float, float]]) -> Callable[[str], float]:
    glat, glon = landmarks[goal]
    def h(node: str) -> float:
        if node not in landmarks:
            return 0.0
        lat, lon = landmarks[node]
        return haversine(lat, lon, glat, glon)
    return h
