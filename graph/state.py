"""
state.py

Define el estado compartido que fluye entre todos los agentes en LangGraph.
Usa Annotated con reducers para soportar ejecución paralela.
"""

from typing import TypedDict, List, Optional, Annotated


def keep_last(current, new):
    """Reducer que conserva el último valor no None"""
    if new is None:
        return current
    return new


class AgentState(TypedDict):
    # Pregunta original del usuario
    question: str

    # Agentes a los que el router decide enviar la pregunta
    agents_to_call: List[str]

    # Resultados de cada agente (Annotated para soportar escritura paralela)
    performance_result: Annotated[Optional[str], keep_last]
    tactical_result: Annotated[Optional[str], keep_last]
    players_result: Annotated[Optional[str], keep_last]
    comparative_result: Annotated[Optional[str], keep_last]

    # Respuesta final consolidada
    final_answer: str