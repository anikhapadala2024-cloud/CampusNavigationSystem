from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import os
from app.graph import get_campus_graph, get_landmarks
from app.astar import a_star
from app.heuristics import make_heuristic
from app.algorithms import dijkstra, bfs, dfs

app = FastAPI(
    title="Campus Navigation System",
    description="AI-powered pathfinding for KL University campus (Vaddeswaram, AP)",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the frontend folder as static files at /frontend
_here = os.path.dirname(os.path.abspath(__file__))
_frontend_dir = os.path.join(_here, "..", "frontend")
if os.path.isdir(_frontend_dir):
    app.mount("/frontend", StaticFiles(directory=_frontend_dir, html=True), name="frontend")


class NavigationRequest(BaseModel):
    start: str
    destination: str


# ---------------------------------------------------------------------------
# GET /
# ---------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def root():
    return HTMLResponse(
        content="""
        <html>
          <head>
            <title>Campus Navigation System</title>
            <meta http-equiv="refresh" content="0; url=/frontend/index.html" />
          </head>
          <body>
            <h2>🏫 KL Campus Navigation System</h2>
            <p>Redirecting to <a href="/frontend/index.html">the interactive map</a>...</p>
            <p>API docs: <a href="/docs">/docs</a></p>
          </body>
        </html>
        """,
        status_code=200,
    )


# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------
@app.get("/health")
def health():
    landmarks = get_landmarks()
    return {"status": "ok", "locations_count": len(landmarks)}


# ---------------------------------------------------------------------------
# GET /locations
# ---------------------------------------------------------------------------
@app.get("/locations")
def locations():
    landmarks = get_landmarks()
    return [
        {"name": name, "lat": lat, "lon": lon}
        for name, (lat, lon) in landmarks.items()
    ]


# ---------------------------------------------------------------------------
# POST /navigate
# ---------------------------------------------------------------------------
@app.post("/navigate")
def navigate(req: NavigationRequest):
    graph = get_campus_graph()
    landmarks = get_landmarks()

    if req.start not in graph:
        raise HTTPException(status_code=404, detail=f"Start location '{req.start}' not found.")
    if req.destination not in graph:
        raise HTTPException(status_code=404, detail=f"Destination '{req.destination}' not found.")

    heuristic = make_heuristic(req.destination, landmarks)
    path, distance, nodes_expanded, trace = a_star(graph, heuristic, req.start, req.destination)

    if path is None:
        raise HTTPException(status_code=404, detail="No path found between the given locations.")

    distance_metres = round(distance, 1)
    # walking speed: 80 m/min  → time = distance / 80  (minutes)
    estimated_walk_time_minutes = round(distance_metres / 80.0, 2)

    return {
        "algorithm": "A*",
        "path": path,
        "distance_metres": distance_metres,
        "nodes_expanded": nodes_expanded,
        "trace": trace,
        "estimated_walk_time_minutes": estimated_walk_time_minutes,
    }


# ---------------------------------------------------------------------------
# POST /compare
# ---------------------------------------------------------------------------
@app.post("/compare")
def compare(req: NavigationRequest):
    graph = get_campus_graph()
    landmarks = get_landmarks()

    if req.start not in graph:
        raise HTTPException(status_code=404, detail=f"Start location '{req.start}' not found.")
    if req.destination not in graph:
        raise HTTPException(status_code=404, detail=f"Destination '{req.destination}' not found.")

    results = {}

    # A*
    heuristic = make_heuristic(req.destination, landmarks)
    path_a, cost_a, exp_a, _ = a_star(graph, heuristic, req.start, req.destination)
    results["A*"] = {
        "path": path_a,
        "cost": round(cost_a, 1) if cost_a is not None else None,
        "nodes_expanded": exp_a,
        "cost_unit": "metres",
    }

    # Dijkstra
    path_d, cost_d, exp_d = dijkstra(graph, req.start, req.destination)
    results["Dijkstra"] = {
        "path": path_d,
        "cost": round(cost_d, 1) if cost_d is not None else None,
        "nodes_expanded": exp_d,
        "cost_unit": "metres",
    }

    # BFS — cost is hops
    path_b, cost_b, exp_b = bfs(graph, req.start, req.destination)
    results["BFS"] = {
        "path": path_b,
        "cost": cost_b,  # integer hops, no rounding needed
        "nodes_expanded": exp_b,
        "cost_unit": "hops",
    }

    # DFS
    path_df, cost_df, exp_df = dfs(graph, req.start, req.destination)
    results["DFS"] = {
        "path": path_df,
        "cost": round(cost_df, 1) if cost_df is not None else None,
        "nodes_expanded": exp_df,
        "cost_unit": "metres",
    }

    return results


# ---------------------------------------------------------------------------
# GET /nearest/{amenity}
# ---------------------------------------------------------------------------
@app.get("/nearest/{amenity}")
def nearest(
    amenity: str,
    from_location: str = Query(..., description="Name of the starting campus location"),
):
    graph = get_campus_graph()
    landmarks = get_landmarks()

    if from_location not in graph:
        raise HTTPException(status_code=404, detail=f"Location '{from_location}' not found.")

    # Find all candidate destinations whose name contains the amenity string
    keyword = amenity.lower()
    candidates = [name for name in landmarks if keyword in name.lower()]

    if not candidates:
        raise HTTPException(
            status_code=404,
            detail=f"No campus location found containing '{amenity}'.",
        )

    # Run A* to each candidate and pick the shortest reachable one
    best_result = None
    best_distance = float("inf")

    for destination in candidates:
        if destination == from_location:
            continue
        heuristic = make_heuristic(destination, landmarks)
        path, distance, nodes_expanded, trace = a_star(graph, heuristic, from_location, destination)
        if path is not None and distance < best_distance:
            best_distance = distance
            best_result = {
                "algorithm": "A*",
                "amenity_query": amenity,
                "nearest_match": destination,
                "from": from_location,
                "path": path,
                "distance_metres": round(distance, 1),
                "nodes_expanded": nodes_expanded,
                "trace": trace,
                "estimated_walk_time_minutes": round(distance / 80.0, 2),
            }

    if best_result is None:
        raise HTTPException(
            status_code=404,
            detail=f"No reachable location containing '{amenity}' from '{from_location}'.",
        )

    return best_result
