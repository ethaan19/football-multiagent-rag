"""
main_graph.py

Grafo principal de LangGraph que:
1. Recibe la pregunta del usuario
2. El router decide qué agentes invocar
3. Los agentes seleccionados se ejecutan secuencialmente
4. Un nodo consolidador une todas las respuestas en una respuesta final
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from langgraph.graph import StateGraph, END
from graph.state import AgentState
from agents.router_agent import router_agent
from agents.performance_agent import performance_agent
from agents.tactical_agent import tactical_agent
from agents.players_agent import players_agent
from agents.comparative_agent import comparative_agent

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01"
)

LLM_MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")

CONSOLIDATOR_SYSTEM_PROMPT = """
You are the final consolidator of a multi-agent football analysis system.
You will receive reports from one or more specialized agents and your task is to merge them
into a single coherent, clear, and well-structured response.

INSTRUCTIONS:
- Always respond in English.
- Integrate all received analyses naturally, without repeating information.
- Remove redundancies but preserve all important data.
- Structure the response with clear sections if there is information from multiple agents.
- Maintain an expert but accessible tone.
- The final response must be complete and self-contained.
- Do not mention that you are a consolidator or that there are multiple agents behind the scenes.
"""


# ─────────────────────────────────────────────
# Nodos intermedios (ejecutan agente si fue seleccionado)
# ─────────────────────────────────────────────

def maybe_run_performance(state: AgentState) -> AgentState:
    if "performance" in state.get("agents_to_call", []):
        return performance_agent(state)
    return state


def maybe_run_tactical(state: AgentState) -> AgentState:
    if "tactical" in state.get("agents_to_call", []):
        return tactical_agent(state)
    return state


def maybe_run_players(state: AgentState) -> AgentState:
    if "players" in state.get("agents_to_call", []):
        return players_agent(state)
    return state


def maybe_run_comparative(state: AgentState) -> AgentState:
    if "comparative" in state.get("agents_to_call", []):
        return comparative_agent(state)
    return state


# ─────────────────────────────────────────────
# Nodo consolidador
# ─────────────────────────────────────────────

def consolidator_node(state: AgentState) -> AgentState:
    print(f"\n🔗 Consolidating responses...")

    if state.get("final_answer"):
        print("⛔ Out of domain question, returning router rejection")
        return state

    results = []

    if state.get("performance_result"):
        results.append(f"[PERFORMANCE ANALYSIS]\n{state['performance_result']}")
    if state.get("tactical_result"):
        results.append(f"[TACTICAL ANALYSIS]\n{state['tactical_result']}")
    if state.get("players_result"):
        results.append(f"[PLAYERS ANALYSIS]\n{state['players_result']}")
    if state.get("comparative_result"):
        results.append(f"[COMPARATIVE ANALYSIS]\n{state['comparative_result']}")

    if len(results) == 1:
        print("✅ Single agent, direct response")
        return {**state, "final_answer": results[0].split("\n", 1)[1]}

    combined = "\n\n".join(results)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": CONSOLIDATOR_SYSTEM_PROMPT},
            {"role": "user", "content": f"Original Question: {state['question']}\n\nAgent Analyses:\n{combined}"}
        ],
        temperature=0.3
    )

    final_answer = response.choices[0].message.content.strip()
    print("✅ Consolidation completed")

    return {**state, "final_answer": final_answer}


# ─────────────────────────────────────────────
# Construcción del grafo (secuencial)
# ─────────────────────────────────────────────

def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    # Añadir nodos
    graph.add_node("router", router_agent)
    graph.add_node("performance", maybe_run_performance)
    graph.add_node("tactical", maybe_run_tactical)
    graph.add_node("players", maybe_run_players)
    graph.add_node("comparative", maybe_run_comparative)
    graph.add_node("consolidator", consolidator_node)

    # Flujo secuencial
    graph.set_entry_point("router")
    graph.add_edge("router", "performance")
    graph.add_edge("performance", "tactical")
    graph.add_edge("tactical", "players")
    graph.add_edge("players", "comparative")
    graph.add_edge("comparative", "consolidator")
    graph.add_edge("consolidator", END)

    return graph.compile()


# ─────────────────────────────────────────────
# Función principal de ejecución
# ─────────────────────────────────────────────

def run_query(question: str) -> str:
    graph = build_graph()

    initial_state: AgentState = {
        "question": question,
        "agents_to_call": [],
        "performance_result": None,
        "tactical_result": None,
        "players_result": None,
        "comparative_result": None,
        "final_answer": ""
    }

    print(f"\n{'='*50}")
    print(f"❓ Question: {question}")
    print(f"{'='*50}")

    result = graph.invoke(initial_state)

    print(f"\n{'='*50}")
    print(f"✨ Final Response:")
    print(f"{'='*50}")
    print(result["final_answer"])

    return result["final_answer"]


if __name__ == "__main__":
    preguntas_test = [
        "How is Real Madrid performing this season?",
        "What players does Arsenal have?",
        "Compare Bayern Munich with Manchester City tactically",
    ]

    for pregunta in preguntas_test:
        run_query(pregunta)
        print("\n")