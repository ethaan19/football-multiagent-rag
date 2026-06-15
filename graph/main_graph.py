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
Eres el consolidador final de un sistema multiagente de análisis de fútbol.
Recibirás los análisis de uno o varios agentes especializados y tu tarea es unirlos
en una única respuesta coherente, clara y bien estructurada.

INSTRUCCIONES:
- Responde siempre en español.
- Integra todos los análisis recibidos de forma natural, sin repetir información.
- Elimina redundancias pero conserva todos los datos importantes.
- Estructura la respuesta con secciones claras si hay información de varios agentes.
- Mantén un tono experto pero accesible.
- La respuesta final debe ser completa y autocontenida.
- No menciones que eres un consolidador ni que hay varios agentes detrás.
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
    print(f"\n🔗 Consolidando respuestas...")

    results = []

    if state.get("performance_result"):
        results.append(f"[ANÁLISIS DE RENDIMIENTO]\n{state['performance_result']}")
    if state.get("tactical_result"):
        results.append(f"[ANÁLISIS TÁCTICO]\n{state['tactical_result']}")
    if state.get("players_result"):
        results.append(f"[ANÁLISIS DE JUGADORES]\n{state['players_result']}")
    if state.get("comparative_result"):
        results.append(f"[ANÁLISIS COMPARATIVO]\n{state['comparative_result']}")

    if len(results) == 1:
        print("✅ Un solo agente, respuesta directa")
        return {**state, "final_answer": results[0].split("\n", 1)[1]}

    combined = "\n\n".join(results)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": CONSOLIDATOR_SYSTEM_PROMPT},
            {"role": "user", "content": f"Pregunta original: {state['question']}\n\nAnálisis de los agentes:\n{combined}"}
        ],
        temperature=0.3
    )

    final_answer = response.choices[0].message.content.strip()
    print("✅ Consolidación completada")

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
    print(f"❓ Pregunta: {question}")
    print(f"{'='*50}")

    result = graph.invoke(initial_state)

    print(f"\n{'='*50}")
    print(f"✨ Respuesta final:")
    print(f"{'='*50}")
    print(result["final_answer"])

    return result["final_answer"]


if __name__ == "__main__":
    preguntas_test = [
        "¿Cómo está rindiendo el Real Madrid esta temporada?",
        "¿Qué jugadores tiene el Arsenal?",
        "Compara tácticamente al Bayern Munich con el Manchester City",
    ]

    for pregunta in preguntas_test:
        run_query(pregunta)
        print("\n")