"""
embed_and_upload.py

Script que:
1. Lee los 3 JSONs generados (teams, players, tactical)
2. Convierte cada registro a texto legible
3. Genera embeddings con Azure OpenAI (text-embedding-3-small)
4. Guarda en ChromaDB (local) en 3 colecciones separadas
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI
import chromadb

load_dotenv()

# Cliente Azure OpenAI
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01"
)

EMBEDDING_MODEL = "text-embedding-3-small"

# Rutas
DATA_DIR = Path("data")
CHROMA_DIR = Path("chroma_db")

# Rutas de los JSONs
TEAMS_FILE = DATA_DIR / "teams_data.json"
PLAYERS_FILE = DATA_DIR / "players_data.json"
TACTICAL_FILE = DATA_DIR / "tactical_data.json"


# ─────────────────────────────────────────────
# Funciones de conversión a texto
# ─────────────────────────────────────────────

def team_to_text(team: dict) -> str:
    return (
        f"Equipo: {team['name']}. "
        f"Liga: {team['league']}. "
        f"Posición actual: {team['position']}. "
        f"Partidos jugados: {team['played_games']}. "
        f"Goles a favor: {team['goals_for']}, Goles en contra: {team['goals_against']}. "
        f"Diferencia de goles: {team['goal_difference']}. "
        f"Puntos: {team['points']}."
    )


def player_to_text(player: dict) -> str:
    """Convierte un jugador a texto legible para embedding"""
    return (
        f"Jugador: {player['name']}. "
        f"Posición: {player['position']}. "
        f"Edad: {player['age']} años. "
        f"Equipo: {player['team_name']}. "
        f"Liga: {player['league']}."
    )


def tactical_to_text(tactical: dict) -> str:
    """Convierte información táctica a texto legible para embedding"""
    characteristics = ", ".join(tactical.get("characteristics", []))
    strengths = ", ".join(tactical.get("strengths", []))
    weaknesses = ", ".join(tactical.get("weaknesses", []))

    return (
        f"Análisis táctico de {tactical['team_name']}. "
        f"Liga: {tactical['league']}. "
        f"Formación: {tactical['formation']}. "
        f"Estilo de juego: {tactical['playstyle']}. "
        f"Características: {characteristics}. "
        f"Puntos fuertes: {strengths}. "
        f"Puntos débiles: {weaknesses}."
    )


# ─────────────────────────────────────────────
# Funciones de embedding
# ─────────────────────────────────────────────

def generate_embedding(text: str) -> list[float]:
    """Genera embedding para un texto usando Azure OpenAI"""
    response = client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL
    )
    return response.data[0].embedding


def generate_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Genera embeddings para una lista de textos en batch"""
    response = client.embeddings.create(
        input=texts,
        model=EMBEDDING_MODEL
    )
    return [item.embedding for item in response.data]


# ─────────────────────────────────────────────
# Funciones de carga en ChromaDB
# ─────────────────────────────────────────────

def load_teams(collection, teams_data: dict) -> None:
    """Carga equipos en ChromaDB"""
    print("📥 Cargando equipos...")

    ids = []
    documents = []
    metadatas = []

    for team_id, team in teams_data.items():
        text = team_to_text(team)
        ids.append(f"team_{team_id}")
        documents.append(text)
        metadatas.append({
            "team_id": str(team_id),
            "team_name": team["name"],
            "league": team["league"],
            "position": team["position"],
            "points": team["points"]
        })

    embeddings = generate_embeddings_batch(documents)

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"✅ {len(ids)} equipos cargados en ChromaDB")


def load_players(collection, players_data: list) -> None:
    """Carga jugadores en ChromaDB"""
    print("📥 Cargando jugadores...")

    # ChromaDB tiene límite de batch, procesamos en grupos de 100
    batch_size = 100

    for i in range(0, len(players_data), batch_size):
        batch = players_data[i:i + batch_size]

        ids = [f"player_{p['id']}" for p in batch]
        documents = [player_to_text(p) for p in batch]
        metadatas = [{
            "player_id": str(p["id"]),
            "player_name": p["name"],
            "position": p["position"],
            "age": p["age"],
            "team_name": p["team_name"],
            "league": p["league"]
        } for p in batch]

        embeddings = generate_embeddings_batch(documents)

        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        print(f"  ✅ Batch {i // batch_size + 1}: {len(batch)} jugadores cargados")

    print(f"✅ {len(players_data)} jugadores cargados en ChromaDB")


def load_tactical(collection, tactical_data: dict) -> None:
    """Carga información táctica en ChromaDB"""
    print("📥 Cargando datos tácticos...")

    ids = []
    documents = []
    metadatas = []

    for team_id, tactical in tactical_data.items():
        text = tactical_to_text(tactical)
        ids.append(f"tactical_{team_id}")
        documents.append(text)
        metadatas.append({
            "team_id": str(team_id),
            "team_name": tactical["team_name"],
            "league": tactical["league"],
            "formation": tactical["formation"],
            "playstyle": tactical["playstyle"]
        })

    embeddings = generate_embeddings_batch(documents)

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"✅ {len(ids)} perfiles tácticos cargados en ChromaDB")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    print("\n🚀 Iniciando proceso de embeddings y carga en ChromaDB...\n")

    # Cargar JSONs
    print("📂 Leyendo archivos JSON...")
    with open(TEAMS_FILE, "r", encoding="utf-8") as f:
        teams_data = json.load(f)
    with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
        players_data = json.load(f)
    with open(TACTICAL_FILE, "r", encoding="utf-8") as f:
        tactical_data = json.load(f)
    print(f"✅ JSONs cargados: {len(teams_data)} equipos, {len(players_data)} jugadores, {len(tactical_data)} tácticos\n")

    # Inicializar ChromaDB
    print("🗄️  Inicializando ChromaDB...")
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Crear colecciones (o resetear si ya existen)
    teams_collection = chroma_client.get_or_create_collection(
        name="teams",
        metadata={"description": "Estadísticas de equipos de las 5 grandes ligas"}
    )
    players_collection = chroma_client.get_or_create_collection(
        name="players",
        metadata={"description": "Información de jugadores por equipo"}
    )
    tactical_collection = chroma_client.get_or_create_collection(
        name="tactical",
        metadata={"description": "Análisis táctico de equipos"}
    )
    print("✅ Colecciones ChromaDB listas\n")

    # Cargar datos
    load_teams(teams_collection, teams_data)
    print()
    load_players(players_collection, players_data)
    print()
    load_tactical(tactical_collection, tactical_data)

    print("\n✨ ¡Proceso completado!")
    print(f"📁 ChromaDB guardado en: {CHROMA_DIR}/")
    print("\n📊 Resumen:")
    print(f"  - Equipos:   {teams_collection.count()} documentos")
    print(f"  - Jugadores: {players_collection.count()} documentos")
    print(f"  - Tácticos:  {tactical_collection.count()} documentos")


if __name__ == "__main__":
    main()