"""
FastAPI backend for Football RAG Multiagent system.
Handles queries and routes them through the multi-agent system.
"""

import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import agents and graph
from graph.main_graph import build_graph

load_dotenv()

app = FastAPI(
    title="Football RAG Multiagent API",
    description="Multi-agent system for analyzing European football",
    version="1.0.0"
)

# ═══════════════════════════════════════════════════════════════
# CORS Configuration
# ═══════════════════════════════════════════════════════════════

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://football-multiagent-rag.vercel.app",
        "*"  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════════
# Request/Response Models
# ═══════════════════════════════════════════════════════════════

class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    answer: str
    agents_used: list[str]


# ═══════════════════════════════════════════════════════════════
# Initialize Graph
# ═══════════════════════════════════════════════════════════════

try:
    graph = build_graph()
    print("✅ LangGraph compiled successfully")
except Exception as e:
    print(f"❌ Error compiling graph: {e}")
    graph = None


# ═══════════════════════════════════════════════════════════════
# Endpoints
# ═══════════════════════════════════════════════════════════════

@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "Football RAG Multiagent API",
        "version": "1.0.0"
    }


@app.post("/query")
async def query(request: QueryRequest) -> QueryResponse:
    """
    Main query endpoint.
    Accepts a football question and returns an answer from the multi-agent system.
    """
    if not graph:
        raise HTTPException(status_code=500, detail="Graph not initialized")
    
    try:
        # Run the graph with the question
        result = graph.invoke({"question": request.question})
        
        # Extract answer and agents used
        answer = result.get("final_answer", "No answer generated")
        agents_used = result.get("agents_to_call", [])
        
        return QueryResponse(
            question=request.question,
            answer=answer,
            agents_used=agents_used
        )
    
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/leagues")
async def get_leagues() -> Dict[str, Any]:
    """Get available leagues."""
    try:
        with open("config/constants.py", "r") as f:
            content = f.read()
            # Extract league names from LEAGUES constant
            if "LEAGUES =" in content:
                # Simple parsing (in production, use proper import)
                leagues = {
                    "La Liga": "🇪🇸 Spain",
                    "Premier League": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 England",
                    "Bundesliga": "🇩🇪 Germany",
                    "Serie A": "🇮🇹 Italy",
                    "Ligue 1": "🇫🇷 France"
                }
                return {"leagues": leagues}
    except Exception as e:
        print(f"Error reading leagues: {e}")
    
    return {
        "leagues": {
            "La Liga": "🇪🇸 Spain",
            "Premier League": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 England",
            "Bundesliga": "🇩🇪 Germany",
            "Serie A": "🇮🇹 Italy",
            "Ligue 1": "🇫🇷 France"
        }
    }


@app.get("/teams")
async def get_teams() -> Dict[str, Any]:
    """Get available teams from generated data."""
    try:
        with open("data/teams_data.json", "r", encoding="utf-8") as f:
            teams_data = json.load(f)
            
        # Group teams by league
        teams_by_league = {}
        for team_id, team_info in teams_data.items():
            league = team_info.get("league", "Unknown")
            if league not in teams_by_league:
                teams_by_league[league] = []
            teams_by_league[league].append({
                "name": team_info.get("name"),
                "position": team_info.get("position"),
                "points": team_info.get("points")
            })
        
        return {"teams": teams_by_league}
    
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Teams data not found. Run 'python fetch_football_data.py' and 'python embed_and_upload.py'"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading teams: {str(e)}")


# ═══════════════════════════════════════════════════════════════
# Error Handlers
# ═══════════════════════════════════════════════════════════════

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }


# ═══════════════════════════════════════════════════════════════
# Startup Event
# ═══════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup_event():
    print("🚀 Football RAG Multiagent API starting...")
    print("📊 Available endpoints:")
    print("  - GET  /          (Health check)")
    print("  - POST /query     (Main query endpoint)")
    print("  - GET  /leagues   (Available leagues)")
    print("  - GET  /teams     (Available teams)")
    print("  - GET  /docs      (Swagger documentation)")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
