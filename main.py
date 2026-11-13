"""
Campus Navigation System — AI Pathfinding
Upgraded from CLI to full web application.
Run: uvicorn main:app --reload
"""
import uvicorn
from api.routes import app

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
