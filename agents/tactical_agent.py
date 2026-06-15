"""
tactical_agent.py

Agente especializado en análisis táctico de equipos.
Consulta la colección 'tactical' de ChromaDB.
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

TACTICAL_SYSTEM_PROMPT = """
Eres un analista táctico experto en fútbol europeo, con un nivel similar al de los mejores analistas de medios especializados.
Tu especialidad es el análisis táctico: formaciones, estilos de juego, presión, transiciones, fortalezas y debilidades.

INSTRUCCIONES:
- Responde siempre en español.
- Basa tu análisis ÚNICAMENTE en el contexto proporcionado.
- Explica los conceptos tácticos de forma clara, incluso para alguien que no sea experto.
- Usa terminología futbolística precisa (pressing, basculación, línea defensiva, etc.).
- Si no tienes suficiente información en el contexto, dilo claramente.
- Estructura tu respuesta con análisis profundo pero conciso.
"""


def search_tactical(query: str, n_results: int = 4) -> str:
    """Busca información táctica relevante en ChromaDB"""
    chroma_client = chromadb.PersistentClient(path="chroma_db")
    collection = chroma_client.get_collection("tactical")

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
    return "\n\n".join(documents) if documents else "No se encontraron datos tácticos relevantes."


def tactical_agent(state: AgentState) -> AgentState:
    """
    Busca información táctica en ChromaDB y genera un análisis táctico.
    """
    question = state["question"]
    print(f"\n🎯 Tactical Agent procesando: '{question}'")

    context = search_tactical(question)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": TACTICAL_SYSTEM_PROMPT},
            {"role": "user", "content": f"Contexto:\n{context}\n\nPregunta: {question}"}
        ],
        temperature=0.3
    )

    result = response.choices[0].message.content.strip()
    print(f"✅ Tactical Agent completado")

    return {**state, "tactical_result": result}