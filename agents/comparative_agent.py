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
You are an elite analyst specializing in European football comparisons.
Your specialty is comparing teams and players objectively, using statistical data and tactical analysis.

INSTRUCTIONS:
- Always respond in English.
- Base your comparison ONLY on the provided context.
- Always structure the comparison in clear sections (statistics, tactics, key players).
- Be objective and balanced, highlighting strengths and weaknesses on each side.
- End with a clear and justified conclusion.
- If you do not have enough information in the context, say so clearly.
- Use tables or lists when they help clarify the comparison.
"""


def search_all_collections(query: str, n_results: int = 4) -> str:
    """Searches all 3 ChromaDB collections and combines the context"""
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

    return "\n\n".join(context_parts) if context_parts else "No relevant data found."


def comparative_agent(state: AgentState) -> AgentState:
    """
    Searches all collections and generates a detailed comparison.
    """
    question = state["question"]
    print(f"\n⚖️  Comparative Agent processing: '{question}'")

    context = search_all_collections(question)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": COMPARATIVE_SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ],
        temperature=0.3
    )

    result = response.choices[0].message.content.strip()
    print(f"✅ Comparative Agent completed")

    return {**state, "comparative_result": result}