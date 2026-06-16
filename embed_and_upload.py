import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI
import chromadb

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01"
)

EMBEDDING_MODEL = "text-embedding-3-small"

# Paths
DATA_DIR = Path("data")
CHROMA_DIR = Path("chroma_db")

# JSON Paths
TEAMS_FILE = DATA_DIR / "teams_data.json"
PLAYERS_FILE = DATA_DIR / "players_data.json"
TACTICAL_FILE = DATA_DIR / "tactical_data.json"


# ─────────────────────────────────────────────
# Text conversion functions (English)
# ─────────────────────────────────────────────

def team_to_text(team: dict) -> str:
    return (
        f"Team: {team['name']}. "
        f"League: {team['league']}. "
        f"Current position: {team['position']}. "
        f"Played games: {team['played_games']}. "
        f"Goals for: {team['goals_for']}, Goals against: {team['goals_against']}. "
        f"Goal difference: {team['goal_difference']}. "
        f"Points: {team['points']}."
    )


def player_to_text(player: dict) -> str:
    """Converts a player to legible text for embedding"""
    return (
        f"Player: {player['name']}. "
        f"Position: {player['position']}. "
        f"Age: {player['age']} years. "
        f"Team: {player['team_name']}. "
        f"League: {player['league']}."
    )


def tactical_to_text(tactical: dict) -> str:
    """Converts tactical information to legible text for embedding"""
    characteristics = ", ".join(tactical.get("characteristics", []))
    strengths = ", ".join(tactical.get("strengths", []))
    weaknesses = ", ".join(tactical.get("weaknesses", []))

    return (
        f"Tactical analysis of {tactical['team_name']}. "
        f"League: {tactical['league']}. "
        f"Formation: {tactical['formation']}. "
        f"Playstyle: {tactical['playstyle']}. "
        f"Characteristics: {characteristics}. "
        f"Strengths: {strengths}. "
        f"Weaknesses: {weaknesses}."
    )


# ─────────────────────────────────────────────
# Embedding functions
# ─────────────────────────────────────────────

def generate_embedding(text: str) -> list[float]:
    """Generates embedding for a text using Azure OpenAI"""
    response = client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL
    )
    return response.data[0].embedding


def generate_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Generates embeddings for a list of texts in batch"""
    response = client.embeddings.create(
        input=texts,
        model=EMBEDDING_MODEL
    )
    return [item.embedding for item in response.data]


# ─────────────────────────────────────────────
# ChromaDB loading functions
# ─────────────────────────────────────────────

def load_teams(collection, teams_data: dict) -> None:
    """Loads teams to ChromaDB"""
    print("📥 Loading teams...")

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

    print(f"✅ {len(ids)} teams loaded into ChromaDB")


def load_players(collection, players_data: list) -> None:
    """Loads players to ChromaDB"""
    print("📥 Loading players...")

    # ChromaDB has a batch size limit, process in groups of 100
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

        print(f"  ✅ Batch {i // batch_size + 1}: {len(batch)} players loaded")

    print(f"✅ {len(players_data)} players loaded into ChromaDB")


def load_tactical(collection, tactical_data: dict) -> None:
    """Loads tactical info to ChromaDB"""
    print("📥 Loading tactical data...")

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

    print(f"✅ {len(ids)} tactical profiles loaded into ChromaDB")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    print("\n🚀 Starting embedding and loading process into ChromaDB...\n")

    # Load JSONs
    print("📂 Reading JSON files...")
    with open(TEAMS_FILE, "r", encoding="utf-8") as f:
        teams_data = json.load(f)
    with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
        players_data = json.load(f)
    with open(TACTICAL_FILE, "r", encoding="utf-8") as f:
        tactical_data = json.load(f)
    print(f"✅ JSONs loaded: {len(teams_data)} teams, {len(players_data)} players, {len(tactical_data)} tactical profiles\n")

    # Initialize ChromaDB
    print("🗄️  Initializing ChromaDB...")
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Reset collections: delete if they exist and recreate
    # (So we don't mix Spanish and English embeddings)
    for col_name in ["teams", "players", "tactical"]:
        try:
            chroma_client.delete_collection(col_name)
            print(f"🗑️ Deleted old collection: {col_name}")
        except Exception:
            pass

    teams_collection = chroma_client.get_or_create_collection(
        name="teams",
        metadata={"description": "Team statistics for the 5 major leagues"}
    )
    players_collection = chroma_client.get_or_create_collection(
        name="players",
        metadata={"description": "Player information per team"}
    )
    tactical_collection = chroma_client.get_or_create_collection(
        name="tactical",
        metadata={"description": "Tactical analysis of teams"}
    )
    print("✅ ChromaDB collections ready\n")

    # Load data
    load_teams(teams_collection, teams_data)
    print()
    load_players(players_collection, players_data)
    print()
    load_tactical(tactical_collection, tactical_data)

    print("\n✨ Process completed!")
    print(f"📁 ChromaDB saved in: {CHROMA_DIR}/")
    print("\n📊 Summary:")
    print(f"  - Teams:     {teams_collection.count()} documents")
    print(f"  - Players:   {players_collection.count()} documents")
    print(f"  - Tactical:  {tactical_collection.count()} documents")


if __name__ == "__main__":
    main()
