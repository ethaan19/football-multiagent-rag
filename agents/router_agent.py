"""
router_agent.py

Agente que analiza la pregunta del usuario y decide
qué agentes especializados deben responderla.
"""

import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from graph.state import AgentState

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01"
)

LLM_MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")

ROUTER_SYSTEM_PROMPT = """
Eres el agente orquestador de un sistema RAG de análisis de fútbol.
Tu única tarea es analizar la pregunta del usuario y decidir qué agentes especializados deben responderla.

Los agentes disponibles son:
- "performance": Para preguntas sobre estadísticas, standings, puntos, victorias, goles, rachas de equipos.
- "tactical": Para preguntas sobre formaciones, estilos de juego, fortalezas y debilidades tácticas de equipos.
- "players": Para preguntas sobre jugadores específicos, sus posiciones, edades o qué jugadores tiene un equipo.
- "comparative": Para preguntas que comparan dos o más equipos o jugadores entre sí.

REGLAS:
- Puedes seleccionar uno o varios agentes si la pregunta lo requiere.
- Si la pregunta compara dos equipos, usa "comparative" junto con los agentes necesarios.
- Responde ÚNICAMENTE con un JSON válido, sin texto adicional, sin markdown, sin explicaciones.

Formato de respuesta:
{"agents": ["performance", "tactical"]}
"""


def router_agent(state: AgentState) -> AgentState:
    """
    Analiza la pregunta y decide qué agentes invocar.
    Actualiza el estado con la lista de agentes a llamar.
    """
    question = state["question"]
    print(f"\n🔀 Router analizando: '{question}'")

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": ROUTER_SYSTEM_PROMPT},
            {"role": "user", "content": f"Pregunta: {question}"}
        ],
        temperature=0
    )

    raw = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(raw)
        agents_to_call = parsed.get("agents", ["performance"])
    except json.JSONDecodeError:
        print(f"⚠️  Error parseando respuesta del router: {raw}")
        agents_to_call = ["performance"]

    print(f"✅ Router decidió: {agents_to_call}")

    return {**state, "agents_to_call": agents_to_call}