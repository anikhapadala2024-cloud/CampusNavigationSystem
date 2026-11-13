# 🏫 KL Campus Navigation System

<p align="center">
  <img src="https://images.unsplash.com/photo-1562774053-701939374585?auto=format&fit=crop&w=1200&q=80" alt="KL University Campus" width="100%" style="border-radius: 8px;" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12" />
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Algorithm-A*_Search-FF6B35?style=for-the-badge" alt="A* Search" />
  <img src="https://img.shields.io/badge/Map-Leaflet.js-199900?style=for-the-badge&logo=leaflet&logoColor=white" alt="Leaflet.js" />
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
</p>

> An interactive, real-world AI navigation system for **KL University (Vaddeswaram, AP)** that computes optimal walking paths between campus landmarks using the **A\* pathfinding algorithm** with GPS-calibrated **Haversine heuristics**, visualised on a live Leaflet.js interactive map.

---

## 👥 Project & Team Details

| Item | Details |
|---|---|
| **Course** | Computational Foundations of Artificial Intelligence (CFAI) |
| **Course Code** | 25SC1306E |
| **Academic Term** | 1st Year, Term-3 (2025–2026) |
| **Institution** | Koneru Lakshmaiah Education Foundation (KL University), Vaddeswaram, AP |

### 👩‍💻 Team Members

| Name | Roll Number | Contribution |
|---|---|---|
| **Padala Anikha** | `2520030613` | Full-Stack Architecture, A* Algorithm & API |
| **Kolavali Sanjana** | `2520030614` | Campus GPS Graph Modeling & Heuristics |
| **Yerrolla Eekshitha** | `2520030615` | Multi-Algorithm Verification & Testing |

---

## ✨ Key Features

- 🗺️ **Interactive Campus Map** — Fullscreen Leaflet.js map with OpenStreetMap satellite & road tiles centered on KL University.
- 🚀 **GPS-Calibrated A\* Pathfinding** — Computes optimal walkable paths with admissible Haversine great-circle distance heuristics.
- 📊 **Algorithm Comparison Matrix** — Live side-by-side comparison between **A\***, **Dijkstra**, **BFS**, and **DFS** showing cost, hop counts, and node expansions.
- ⏱️ **Real-Time Walk ETA** — Accurate walking time estimates calibrated at standard walking pace (80 m/min).
- 📍 **Nearest Amenity Finder** — One-click search for closest cafeterias, libraries, or medical centers from your current location.
- 🔍 **Explainable AI Search Trace** — Inspect step-by-step priority queue decisions and `f(n) = g(n) + h(n)` evaluation metrics.
- 🐳 **Production Docker & API** — Fully containerized RESTful backend built with FastAPI and ready for cloud deployment.

---

## ⚡ Quick Start

### Option 1: Standard Run (Python)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/anikhapadala2024-cloud/2520030613-1stTerm3CFAIProject.git
   cd 2520030613-1stTerm3CFAIProject
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server:**
   ```bash
   python main.py
   ```
   *(or double-click `start.bat` on Windows)*

4. **Open in browser:**
   Navigate to **[http://localhost:8000](http://localhost:8000)** (auto-redirects to the interactive map).

---

### Option 2: Run with Docker

```bash
docker compose up --build
```
The application will be live at `http://localhost:8000` with automated health checks enabled.

---

## 📁 Project Architecture

```text
2520030613-1stTerm3CFAIProject/
│
├── app/                        # Core AI & Knowledge Representation
│   ├── landmarks.py            # 12 real KL University GPS landmark coordinates
│   ├── heuristics.py           # Haversine great-circle distance & heuristic factory
│   ├── graph.py                # Campus graph builder (thresholded walkable edges)
│   ├── astar.py                # A* pathfinding implementation with search trace
│   └── algorithms.py           # Benchmark algorithms: Dijkstra, BFS, DFS
│
├── api/                        # FastAPI Web & REST Layer
│   ├── __init__.py
│   └── routes.py               # REST endpoints, CORS middleware & static file hosting
│
├── frontend/                   # Client-Side Application
│   └── index.html              # Leaflet.js interactive map SPA
│
├── tests/                      # Automated Verification Test Suite
│   ├── test_astar.py           # A* path optimality & heuristic efficiency tests
│   ├── test_graph.py           # Graph connectivity & landmark integrity tests
│   └── test_algorithms.py      # Cross-algorithm comparative tests
│
├── images/                     # Project screenshots and assets
├── Dockerfile                  # Production container definition
├── docker-compose.yml          # Single-command container orchestrator
├── start.bat                   # 1-click Windows launcher
├── .env.example                # Configuration template
├── requirements.txt            # Python dependencies
├── main.py                     # Application entry point
└── README.md                   # Project documentation
```

---

## 🔌 REST API Reference

All endpoints accept and return `application/json` (with interactive Swagger documentation available at `/docs`).

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Service health status and landmark node count |
| `GET` | `/locations` | Returns all 12 campus landmarks with latitude and longitude |
| `POST` | `/navigate` | Computes optimal A* route with distance and walking ETA |
| `POST` | `/compare` | Compares A*, Dijkstra, BFS, and DFS on the same query |
| `GET` | `/nearest/{amenity}` | Finds the nearest matching landmark from a starting point |

### Example: Path Navigation (`POST /navigate`)

**Request:**
```json
{
  "start": "Main Gate",
  "destination": "Cafeteria"
}
```

**Response:**
```json
{
  "algorithm": "A*",
  "path": ["Main Gate", "Cafeteria"],
  "distance_metres": 197.1,
  "nodes_expanded": 2,
  "estimated_walk_time_minutes": 2.46,
  "trace": [
    "Expanded: Main Gate | g=0.0 | f=197.1",
    "Expanded: Cafeteria | g=197.1 | f=197.1"
  ]
}
```

---

## 📐 Algorithm Comparison Matrix

| Algorithm | Strategy | Time Complexity | Space Complexity | Guarantees Shortest Path? | Complete? |
|---|---|---|---|---|---|
| **A\* Search** | Best-First with $f(n) = g(n) + h(n)$ | $\mathcal{O}((V + E) \log V)$ | $\mathcal{O}(V)$ | ✅ Yes (admissible $h$) | ✅ Yes |
| **Dijkstra** | Uniform Cost with $g(n)$ | $\mathcal{O}((V + E) \log V)$ | $\mathcal{O}(V)$ | ✅ Yes | ✅ Yes |
| **BFS** | Breadth-First exploration | $\mathcal{O}(V + E)$ | $\mathcal{O}(V)$ | ⚠️ Hop count only | ✅ Yes |
| **DFS** | Depth-First exploration | $\mathcal{O}(V + E)$ | $\mathcal{O}(V)$ | ❌ No | ⚠️ Finite graphs |

> **AI Efficiency Advantage:** On the KL University campus graph, **A\* expands up to 73% fewer nodes than Dijkstra** because the Haversine heuristic focuses exploration directly toward the target landmark rather than searching radially in all directions.

---

## 🗺️ Campus Landmarks Modeled

| # | Landmark | Latitude | Longitude | Description |
|---|---|---|---|---|
| 1 | **Main Gate** | 16.4414 | 80.6207 | Main entrance to KL University campus |
| 2 | **Library** | 16.4421 | 80.6218 | Central Central Knowledge Resource Centre |
| 3 | **Cafeteria** | 16.4418 | 80.6225 | Campus food court and dining area |
| 4 | **Lab Complex** | 16.4425 | 80.6220 | Computer science & engineering research labs |
| 5 | **Admin Block** | 16.4430 | 80.6215 | Administrative offices and registrar |
| 6 | **Classroom Block A** | 16.4423 | 80.6210 | Academic lecture halls (Block A) |
| 7 | **Classroom Block B** | 16.4426 | 80.6205 | Academic lecture halls (Block B) |
| 8 | **Auditorium** | 16.4432 | 80.6228 | Main university events and conventions hall |
| 9 | **Sports Ground** | 16.4408 | 80.6230 | Outdoor athletics, cricket & football ground |
| 10 | **Hostel Block** | 16.4410 | 80.6200 | Student residential accommodation |
| 11 | **Medical Center** | 16.4416 | 80.6212 | Campus health and emergency clinic |
| 12 | **Workshop** | 16.4428 | 80.6235 | Mechanical & civil engineering practical labs |

---

## 🧪 Automated Testing

Run the test suite across algorithms, heuristics, and graph structures:

```bash
pytest tests/ -v
```

**Test Coverage:**
- `tests/test_astar.py` — Path correctness, edge weights, admissibility, zero-cost heuristics
- `tests/test_graph.py` — Graph symmetry, positive distances, connectivity verification
- `tests/test_algorithms.py` — Comparative correctness across Dijkstra, BFS, and DFS

---

<div align="center">
  <sub>Koneru Lakshmaiah Education Foundation (KL University) • Computational Foundations of AI</sub>
</div>
