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
You are an expert tactical analyst in European football, with a level comparable to top analysts in specialized media.
Your specialty is tactical analysis: formations, playstyles, pressing, transitions, strengths, and weaknesses.

INSTRUCTIONS:
- Always respond in English.
- Base your analysis ONLY on the provided context.
- Explain tactical concepts clearly, even for non-experts.
- Use precise football terminology (pressing, shifting, defensive line, etc.).
- If you do not have enough information in the context, say so clearly.
- Structure your response with a deep yet concise analysis.
"""


def search_tactical(query: str, n_results: int = 4) -> str:
    """Searches for relevant tactical information in ChromaDB"""
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
    return "\n\n".join(documents) if documents else "No relevant tactical data found."


def tactical_agent(state: AgentState) -> AgentState:
    """
    Searches for tactical information in ChromaDB and generates a tactical analysis.
    """
    question = state["question"]
    print(f"\n🎯 Tactical Agent processing: '{question}'")

    context = search_tactical(question)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": TACTICAL_SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ],
        temperature=0.3
    )

    result = response.choices[0].message.content.strip()
    print(f"✅ Tactical Agent completed")

    return {**state, "tactical_result": result}