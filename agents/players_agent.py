"""
players_agent.py

Agente especializado en información de jugadores.
Consulta la colección 'players' de ChromaDB.
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import chromadb
from graph.state import AgentState

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01"
)

LLM_MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
EMBEDDING_MODEL = "text-embedding-3-small"

PLAYERS_SYSTEM_PROMPT = """
You are a top-tier European football player scout and analyst.
Your specialty is detailed player knowledge: positions, characteristics, teams, and leagues.

INSTRUCTIONS:
- Always respond in English.
- Base your response ONLY on the provided context.
- Be specific with player names, positions, and teams.
- If asked about a team's squad, list the players in an organized manner by position.
- If you do not have enough information in the context, say so clearly.
- Use an expert yet accessible tone.
"""


def search_players(query: str, n_results: int = 40) -> str:
    """Searches for relevant players in ChromaDB"""
    chroma_client = chromadb.PersistentClient(path="chroma_db")
    collection = chroma_client.get_collection("players")

    embedding_response = client.embeddings.create(
        input=query,
        model=EMBEDDING_MODEL
    )
    query_embedding = embedding_response.data[0].embedding

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    documents = results.get("documents", [[]])[0]
    return "\n\n".join(documents) if documents else "No relevant players found."


def players_agent(state: AgentState) -> AgentState:
    """
    Searches for player information in ChromaDB and generates a detailed response.
    """
    question = state["question"]
    print(f"\n⚽ Players Agent processing: '{question}'")

    context = search_players(question)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": PLAYERS_SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ],
        temperature=0.3
    )

    result = response.choices[0].message.content.strip()
    print(f"✅ Players Agent completed")

    return {**state, "players_result": result}