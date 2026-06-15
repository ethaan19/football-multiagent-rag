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
Eres un scout y analista de jugadores de fútbol europeo de primer nivel.
Tu especialidad es el conocimiento detallado de jugadores: posiciones, características, equipos y ligas.

INSTRUCCIONES:
- Responde siempre en español.
- Basa tu respuesta ÚNICAMENTE en el contexto proporcionado.
- Sé específico con los nombres, posiciones y equipos de los jugadores.
- Si te preguntan por el plantel de un equipo, lista los jugadores de forma organizada por posición.
- Si no tienes suficiente información en el contexto, dilo claramente.
- Usa un tono experto pero accesible.
"""


def search_players(query: str, n_results: int = 40) -> str:
    """Busca jugadores relevantes en ChromaDB"""
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
    return "\n\n".join(documents) if documents else "No se encontraron jugadores relevantes."


def players_agent(state: AgentState) -> AgentState:
    """
    Busca información de jugadores en ChromaDB y genera una respuesta detallada.
    """
    question = state["question"]
    print(f"\n⚽ Players Agent procesando: '{question}'")

    context = search_players(question)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": PLAYERS_SYSTEM_PROMPT},
            {"role": "user", "content": f"Contexto:\n{context}\n\nPregunta: {question}"}
        ],
        temperature=0.3
    )

    result = response.choices[0].message.content.strip()
    print(f"✅ Players Agent completado")

    return {**state, "players_result": result}