"""
router_agent.py

Agente que analiza la pregunta del usuario y decide:
1. Si es sobre fútbol (validación de dominio)
2. Qué agentes especializados deben responderla
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

# ═══════════════════════════════════════════════════════════════
# VALIDATION PROMPT
# ═══════════════════════════════════════════════════════════════

VALIDATION_SYSTEM_PROMPT = """
You are a domain validator for a football analysis system.
Your task is to determine if a question is about European football.

Football-related questions include:
- Team standings, points, statistics, performance
- Player information, squads, transfers
- Tactics, formations, playstyles
- Comparisons between teams or players
- League information, matches, results
- Anything specifically about the 5 major European leagues:
  La Liga, Premier League, Bundesliga, Serie A, Ligue 1

Out-of-domain questions include:
- Diet, health, fitness advice
- General knowledge not about football
- Technical support
- Other sports
- Any topic unrelated to European football

Respond with ONLY "yes" or "no". Nothing else.
"""

# ═══════════════════════════════════════════════════════════════
# ROUTING PROMPT
# ═══════════════════════════════════════════════════════════════

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

# ═══════════════════════════════════════════════════════════════
# OUT OF DOMAIN MESSAGE
# ═══════════════════════════════════════════════════════════════

OUT_OF_DOMAIN_MESSAGE = """❌ I can only answer questions about European football.

I specialize in:
- Team statistics and performance (La Liga, Premier League, Bundesliga, Serie A, Ligue 1)
- Player information and squads
- Tactical analysis (formations, playstyles)
- Team comparisons

Please ask about these topics instead. For example:
- "How is Real Madrid performing this season?"
- "What players does Arsenal have?"
- "How does Bayern Munich play tactically?"
- "Compare PSG and Manchester City"
"""


# ═══════════════════════════════════════════════════════════════
# VALIDATION FUNCTION
# ═══════════════════════════════════════════════════════════════

def validate_football_question(question: str) -> bool:
    """
    Validates if the question is about football.
    Returns True if football-related, False otherwise.
    """
    print(f"\n🔍 Validando dominio...")
    
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": VALIDATION_SYSTEM_PROMPT},
            {"role": "user", "content": f"Question: {question}"}
        ],
        temperature=0,
        max_tokens=5
    )
    
    answer = response.choices[0].message.content.strip().lower()
    is_valid = answer == "yes"
    
    if is_valid:
        print(f"✅ Pregunta válida (sobre fútbol)")
    else:
        print(f"❌ Pregunta fuera de dominio")
    
    return is_valid


# ═══════════════════════════════════════════════════════════════
# ROUTING FUNCTION
# ═══════════════════════════════════════════════════════════════

def route_to_agents(question: str) -> list[str]:
    """
    Routes the question to appropriate specialized agents.
    Returns a list of agent names to activate.
    """
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
    return agents_to_call


# ═══════════════════════════════════════════════════════════════
# MAIN ROUTER AGENT FUNCTION
# ═══════════════════════════════════════════════════════════════

def router_agent(state: AgentState) -> AgentState:
    """
    Main router agent function.
    
    1. Validates if question is about football
    2. If yes: Routes to appropriate agents
    3. If no: Returns out-of-domain message
    
    Updates the state with agents_to_call and final_answer (if out-of-domain).
    """
    question = state["question"]
    
    # STEP 1: Domain validation
    is_football_question = validate_football_question(question)
    
    # STEP 2: If out of domain, reject immediately
    if not is_football_question:
        print(f"⛔ Pregunta rechazada por estar fuera de dominio")
        return {
            **state,
            "agents_to_call": [],
            "final_answer": OUT_OF_DOMAIN_MESSAGE
        }
    
    # STEP 3: Route to appropriate agents
    agents_to_call = route_to_agents(question)
    
    return {
        **state,
        "agents_to_call": agents_to_call
    }