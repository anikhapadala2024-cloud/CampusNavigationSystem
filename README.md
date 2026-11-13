# 🏫 KL Campus Navigation System

<p align="center">
  <img src="https://images.unsplash.com/photo-1562774053-701939374585?auto=format&fit=crop&w=1200&q=80" alt="KL Campus" width="100%" style="border-radius: 8px;" />
</p>

![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)
![A* Search](https://img.shields.io/badge/Algorithm-A*%20Search-FF6B35?style=flat-square)
![Leaflet.js](https://img.shields.io/badge/Map-Leaflet.js-199900?style=flat-square&logo=leaflet&logoColor=white)

> An intelligent campus navigation web app for **KL University (Vaddeswaram, AP)** that finds the shortest walking path between campus landmarks using the A\* pathfinding algorithm, visualised on an interactive map.

---

## 👩‍💻 Team Members

| Name | Roll Number |
|------|------------|
| **Padala Anikha** | 2520030613 |
| **Kolavali Sanjana** | 2520030614 |
| **Yerrolla Eekshitha** | 2520030615 |

---

## 📚 Course Details

- **Course:** Computational Foundations of Artificial Intelligence (CFAI)
- **Course Code:** 25SC1306E
- **Semester:** Term-3 (1st Year)
- **Institution:** KL University (KLEF), Vaddeswaram, Guntur, AP
- **Academic Year:** 2025–26

---

## ✨ Features

- 🗺️ **Interactive Map** — Real KL University campus map rendered with Leaflet.js; click to set source & destination
- 🚀 **A\* Pathfinding** — Optimal shortest-path search using GPS-calibrated Haversine heuristic
- 📊 **Algorithm Comparison** — Side-by-side comparison of A\*, Dijkstra, BFS, and DFS on the same query
- ⏱️ **Walking Time Estimate** — Automatic ETA at average walking speed (1.4 m/s ≈ 5 km/h)
- 📍 **Nearest Amenity Finder** — One-click "Find nearest cafeteria / medical center / hostel" feature
- 🔍 **Step-by-Step Trace** — Expandable panel showing every node A\* opened and its f/g scores
- 🌐 **REST API** — Clean FastAPI backend; integrate with any frontend or mobile app

---

## 📁 Project Structure

```
2520030613-1stTerm3CFAIProject-main/
│
├── app/                        # Core Python package
│   ├── __init__.py
│   ├── landmarks.py            # 12 KL University GPS coordinates
│   ├── heuristics.py           # Haversine distance + heuristic factory
│   ├── graph.py                # Campus adjacency graph builder (≤ 400 m edges)
│   ├── astar.py                # A* search implementation
│   └── algorithms.py           # Dijkstra, BFS, DFS implementations
│
├── api/                        # FastAPI application layer
│   ├── __init__.py
│   └── routes.py               # All route handlers + CORS config
│
├── frontend/                   # Static web UI
│   └── index.html              # Interactive Leaflet.js map (single-page app)
│
├── tests/                      # pytest test suite
│   ├── __init__.py
│   ├── test_astar.py           # A* algorithm tests
│   ├── test_graph.py           # Graph builder & landmark tests
│   └── test_algorithms.py      # Comparative algorithm tests
│
├── main.py                     # Uvicorn entry point
├── requirements.txt            # Python dependencies
└── README.md
```

---

## ⚡ Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the server

```bash
uvicorn main:app --reload
```

### 3. Open the app

Navigate to **http://localhost:8000/frontend/index.html** in your browser.

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check — returns `{"status": "ok"}` |
| `GET` | `/health` | Detailed health status of all services |
| `GET` | `/locations` | List all campus landmarks with GPS coordinates |
| `POST` | `/navigate` | Find shortest path via A\*; returns path, cost, walk time, trace |
| `POST` | `/compare` | Run A\*, Dijkstra, BFS, DFS on same query and compare results |
| `GET` | `/nearest/{amenity}` | Find the nearest landmark matching the given amenity keyword |

### POST `/navigate` — Request body

```json
{
  "start": "Main Gate",
  "end": "Library"
}
```

### POST `/navigate` — Response

```json
{
  "path": ["Main Gate", "Medical Center", "Library"],
  "cost": 142.3,
  "walk_time_seconds": 101,
  "nodes_expanded": 5,
  "trace": ["Expanded: Main Gate | g=0.0 | f=118.2", "..."]
}
```

---

## 📐 Algorithm Comparison

| Algorithm | Time Complexity | Space Complexity | Optimal? | Complete? |
|-----------|----------------|-----------------|----------|-----------|
| **A\*** | O((V + E) log V) | O(V) | ✅ Yes (admissible h) | ✅ Yes |
| **Dijkstra** | O((V + E) log V) | O(V) | ✅ Yes | ✅ Yes |
| **BFS** | O(V + E) | O(V) | ⚠️ Hop-count only | ✅ Yes |
| **DFS** | O(V + E) | O(V) | ❌ No | ⚠️ Finite graphs |

> **Why A\*?** On the campus graph, A\* typically expands 30–50% fewer nodes than Dijkstra because the Haversine heuristic guides the search directly toward the goal, reducing wasted exploration.

---

## 🛠️ Technologies Used

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.12, FastAPI 0.115, Uvicorn |
| **Algorithms** | A\* Search, Dijkstra, BFS, DFS |
| **Heuristic** | Haversine great-circle distance |
| **Map / Frontend** | Leaflet.js, OpenStreetMap tiles, Vanilla JS |
| **Data Validation** | Pydantic v2 |
| **Testing** | pytest 8 |
| **HTTP Client** | HTTPX (for API integration tests) |

---

## 🗺️ Campus Landmarks

The system models **12 real KL University (Vaddeswaram) landmarks** with accurate GPS coordinates:

| Landmark | Latitude | Longitude |
|----------|----------|-----------|
| Main Gate | 16.4414 | 80.6207 |
| Library | 16.4421 | 80.6218 |
| Cafeteria | 16.4418 | 80.6225 |
| Lab Complex | 16.4425 | 80.6220 |
| Admin Block | 16.4430 | 80.6215 |
| Classroom Block A | 16.4423 | 80.6210 |
| Classroom Block B | 16.4426 | 80.6205 |
| Auditorium | 16.4432 | 80.6228 |
| Sports Ground | 16.4408 | 80.6230 |
| Hostel Block | 16.4410 | 80.6200 |
| Medical Center | 16.4416 | 80.6212 |
| Workshop | 16.4428 | 80.6235 |

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

Expected output: **15 tests passing** across 3 test modules.

---

## 👨‍🎓 Academic Context

> **Built as CFAI Term 3 Project | 2520030613 | KL University**
>
> *Computer Fundamentals and AI (CFAI) — 1st Year, Term 3*
> *K L University, Vaddeswaram, Guntur, Andhra Pradesh — 2024–25*
