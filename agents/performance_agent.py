"""
performance_agent.py

Agente especializado en estadísticas y rendimiento de equipos.
Consulta la colección 'teams' de ChromaDB.
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

PERFORMANCE_SYSTEM_PROMPT = """
Eres un analista experto en estadísticas de fútbol europeo.
Tu especialidad son los datos de rendimiento de equipos: posiciones en la tabla, puntos, victorias, derrotas, goles.

Tienes acceso a datos reales de las 5 grandes ligas europeas (La Liga, Premier League, Bundesliga, Serie A, Ligue 1).

INSTRUCCIONES:
- Responde siempre en español.
- Basa tu respuesta ÚNICAMENTE en el contexto proporcionado.
- Sé preciso con los números y estadísticas.
- Si no tienes suficiente información en el contexto, dilo claramente.
- Usa un tono analítico pero accesible.
- Estructura tu respuesta de forma clara y concisa.
"""


def search_teams(query: str, n_results: int = 4) -> str:
    """Busca equipos relevantes en ChromaDB según la query"""
    chroma_client = chromadb.PersistentClient(path="chroma_db")
    collection = chroma_client.get_collection("teams")

    # Generar embedding de la query
    embedding_response = client.embeddings.create(
        input=query,
        model=EMBEDDING_MODEL
    )
    query_embedding = embedding_response.data[0].embedding

    # Buscar en ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    # Formatear resultados
    documents = results.get("documents", [[]])[0]
    return "\n\n".join(documents) if documents else "No se encontraron datos relevantes."


def performance_agent(state: AgentState) -> AgentState:
    """
    Busca estadísticas de equipos en ChromaDB y genera una respuesta analítica.
    """
    question = state["question"]
    print(f"\n📊 Performance Agent procesando: '{question}'")

    # Buscar contexto relevante
    context = search_teams(question)

    # Generar respuesta con LLM
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": PERFORMANCE_SYSTEM_PROMPT},
            {"role": "user", "content": f"Contexto:\n{context}\n\nPregunta: {question}"}
        ],
        temperature=0.3
    )

    result = response.choices[0].message.content.strip()
    print(f"✅ Performance Agent completado")

    return {**state, "performance_result": result}