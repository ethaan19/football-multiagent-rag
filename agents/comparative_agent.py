"""
comparative_agent.py

Agente especializado en comparativas entre equipos o jugadores.
Combina datos de las 3 colecciones de ChromaDB.
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

COMPARATIVE_SYSTEM_PROMPT = """
Eres un analista de élite especializado en comparativas de fútbol europeo.
Tu especialidad es comparar equipos y jugadores de forma objetiva, usando datos estadísticos y análisis táctico.

INSTRUCCIONES:
- Responde siempre en español.
- Basa tu comparativa ÚNICAMENTE en el contexto proporcionado.
- Estructura siempre la comparativa en secciones claras (estadísticas, táctica, jugadores clave).
- Sé objetivo y equilibrado, destacando puntos fuertes y débiles de cada lado.
- Termina con una conclusión clara y justificada.
- Si no tienes suficiente información en el contexto, dilo claramente.
- Usa tablas o listas cuando ayuden a clarificar la comparativa.
"""


def search_all_collections(query: str, n_results: int = 4) -> str:
    """Busca en las 3 colecciones de ChromaDB y combina el contexto"""
    chroma_client = chromadb.PersistentClient(path="chroma_db")

    embedding_response = client.embeddings.create(
        input=query,
        model=EMBEDDING_MODEL
    )
    query_embedding = embedding_response.data[0].embedding

    context_parts = []

    for collection_name in ["teams", "players", "tactical"]:
        collection = chroma_client.get_collection(collection_name)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        documents = results.get("documents", [[]])[0]
        if documents:
            context_parts.append(f"=== {collection_name.upper()} ===\n" + "\n\n".join(documents))

    return "\n\n".join(context_parts) if context_parts else "No se encontraron datos relevantes."


def comparative_agent(state: AgentState) -> AgentState:
    """
    Busca en todas las colecciones y genera una comparativa detallada.
    """
    question = state["question"]
    print(f"\n⚖️  Comparative Agent procesando: '{question}'")

    context = search_all_collections(question)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": COMPARATIVE_SYSTEM_PROMPT},
            {"role": "user", "content": f"Contexto:\n{context}\n\nPregunta: {question}"}
        ],
        temperature=0.3
    )

    result = response.choices[0].message.content.strip()
    print(f"✅ Comparative Agent completado")

    return {**state, "comparative_result": result}