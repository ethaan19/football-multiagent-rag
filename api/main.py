"""
main.py

API FastAPI que expone el sistema RAG multiagente de fútbol.
Endpoints:
- GET  /           → Health check
- POST /query      → Pregunta al sistema multiagente
- GET  /leagues    → Lista de ligas disponibles
- GET  /teams      → Lista de equipos disponibles
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph.main_graph import run_query
from config.constants import LEAGUES
import json
from pathlib import Path

app = FastAPI(
    title="Football RAG Multiagent API",
    description="Sistema RAG multiagéntico para análisis de fútbol europeo",
    version="1.0.0"
)

# CORS para poder conectar con cualquier frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# Modelos de request/response
# ─────────────────────────────────────────────

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    agents_used: list[str] = []


# ─────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────

@app.get("/")
def health_check():
    """Health check"""
    return {
        "status": "ok",
        "message": "Football RAG Multiagent API funcionando 🚀",
        "version": "1.0.0"
    }


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    """
    Endpoint principal. Recibe una pregunta y devuelve
    la respuesta del sistema multiagente.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")

    try:
        answer = run_query(request.question)
        return QueryResponse(
            question=request.question,
            answer=answer
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el sistema: {str(e)}")


@app.get("/leagues")
def get_leagues():
    """Devuelve las ligas disponibles en el sistema"""
    return {
        "leagues": list(LEAGUES.keys()),
        "total": len(LEAGUES)
    }


@app.get("/teams")
def get_teams():
    """Devuelve los equipos disponibles en el sistema"""
    teams_file = Path("data/teams_data.json")

    if not teams_file.exists():
        raise HTTPException(
            status_code=404,
            detail="No se encontraron datos de equipos. Ejecuta primero fetch_football_data.py"
        )

    with open(teams_file, "r", encoding="utf-8") as f:
        teams_data = json.load(f)

    teams_list = [
        {
            "id": team["id"],
            "name": team["name"],
            "league": team["league"],
            "position": team["position"],
            "points": team["points"]
        }
        for team in teams_data.values()
    ]

    # Ordenar por liga y posición
    teams_list.sort(key=lambda x: (x["league"], x["position"]))

    return {
        "teams": teams_list,
        "total": len(teams_list)
    }