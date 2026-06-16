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
You are an expert analyst in European football statistics.
Your specialty is team performance data: table standings, points, wins, losses, goals.

You have access to real data from the 5 major European leagues (La Liga, Premier League, Bundesliga, Serie A, Ligue 1).

INSTRUCTIONS:
- Always respond in English.
- Base your response ONLY on the provided context.
- Be precise with numbers and statistics.
- If you do not have enough information in the context, say so clearly.
- Use an analytical yet accessible tone.
- Structure your response clearly and concisely.
"""


def search_teams(query: str, n_results: int = 4) -> str:
    """Searches for relevant teams in ChromaDB based on the query"""
    chroma_client = chromadb.PersistentClient(path="chroma_db")
    collection = chroma_client.get_collection("teams")

    # Generate query embedding
    embedding_response = client.embeddings.create(
        input=query,
        model=EMBEDDING_MODEL
    )
    query_embedding = embedding_response.data[0].embedding

    # Search in ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    # Format results
    documents = results.get("documents", [[]])[0]
    return "\n\n".join(documents) if documents else "No relevant data found."


def performance_agent(state: AgentState) -> AgentState:
    """
    Searches for team statistics in ChromaDB and generates an analytical response.
    """
    question = state["question"]
    print(f"\n📊 Performance Agent processing: '{question}'")

    # Search for relevant context
    context = search_teams(question)

    # Generate response with LLM
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": PERFORMANCE_SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ],
        temperature=0.3
    )

    result = response.choices[0].message.content.strip()
    print(f"✅ Performance Agent completed")

    return {**state, "performance_result": result}