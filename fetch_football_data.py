"""
fetch_football_data.py

Script que:
1. Conecta a Free API Live Football Data (RapidAPI)
2. Extrae top 4 de cada liga (5 grandes)
3. Extrae jugadores reales de cada equipo
4. Genera información táctica automáticamente
5. Guarda teams_data.json, players_data.json y tactical_data.json
"""

import json
import requests
import os
import time
from pathlib import Path
from typing import Dict, List, Any
from dotenv import load_dotenv
from config.constants import LEAGUES, TACTICAL_INFO

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
FOOTBALL_DATA_API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

# Rutas
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

TEAMS_OUTPUT = DATA_DIR / "teams_data.json"
PLAYERS_OUTPUT = DATA_DIR / "players_data.json"
TACTICAL_OUTPUT = DATA_DIR / "tactical_data.json"

# Headers RapidAPI
RAPIDAPI_HEADERS = {
    "Content-Type": "application/json",
    "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com",
    "x-rapidapi-key": RAPIDAPI_KEY
}

RAPIDAPI_BASE = "https://free-api-live-football-data.p.rapidapi.com"

# IDs de ligas en esta API
LEAGUE_IDS = {
    "La Liga": 87,
    "Premier League": 47,
    "Bundesliga": 54,
    "Serie A": 55,
    "Ligue 1": 53
}

# Mapeo de posiciones
POSITION_MAP = {
    "keepers": "GK",
    "defenders": "DEF",
    "midfielders": "MID",
    "attackers": "FWD",
    "coach": None
}


# ─────────────────────────────────────────────
# Fetch standings
# ─────────────────────────────────────────────

def fetch_standings(league_name: str, league_id: int) -> List[Dict[str, Any]]:
    """Extrae el top 4 de una liga desde RapidAPI"""
    url = f"{RAPIDAPI_BASE}/football-get-standing-all?leagueid={league_id}"
    response = requests.get(url, headers=RAPIDAPI_HEADERS)

    if response.status_code != 200:
        print(f"❌ Error fetching {league_name}: {response.status_code}")
        return []

    data = response.json()
    standing = data.get("response", {}).get("standing", [])

    if not standing:
        print(f"⚠️  Sin datos para {league_name}")
        return []

    top_4 = standing[:4]
    print(f"✅ {league_name}: {len(top_4)} equipos obtenidos")
    return top_4


# ─────────────────────────────────────────────
# Fetch players
# ─────────────────────────────────────────────

def fetch_players(team_id: int, team_name: str) -> List[Dict[str, Any]]:
    """Extrae jugadores reales de un equipo desde RapidAPI"""
    url = f"{RAPIDAPI_BASE}/football-get-list-player?teamid={team_id}"
    response = requests.get(url, headers=RAPIDAPI_HEADERS)

    if response.status_code != 200:
        print(f"  ❌ Error fetching players for {team_name}: {response.status_code}")
        return []

    data = response.json()
    squad = data.get("response", {}).get("list", {}).get("squad", [])

    players = []
    for group in squad:
        title = group.get("title", "")
        position = POSITION_MAP.get(title)

        if position is None:
            continue

        for member in group.get("members", []):
            players.append({
                "id": member.get("id"),
                "name": member.get("name"),
                "position": position,
                "age": member.get("age"),
                "nationality": member.get("cname"),
                "rating": member.get("rating"),
                "goals": member.get("goals", 0),
                "assists": member.get("assists", 0)
            })

    print(f"  ✅ {team_name}: {len(players)} jugadores obtenidos")
    return players


# ─────────────────────────────────────────────
# Generar datos
# ─────────────────────────────────────────────

def generate_teams_data(all_standings: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """Genera diccionario de equipos con sus datos"""
    teams_data = {}

    for league_name, standings in all_standings.items():
        for team in standings:
            team_id = str(team.get("id"))
            scores = team.get("scoresStr", "0-0").split("-")
            goals_for = int(scores[0]) if len(scores) == 2 else 0
            goals_against = int(scores[1]) if len(scores) == 2 else 0

            teams_data[team_id] = {
                "id": team.get("id"),
                "name": team.get("name"),
                "league": league_name,
                "position": team.get("idx"),
                "played_games": team.get("played"),
                "wins": team.get("wins", 0) or 0,
                "draws": team.get("draws", 0) or 0,
                "losses": team.get("losses", 0) or 0,
                "goals_for": goals_for,
                "goals_against": goals_against,
                "goal_difference": team.get("goalConDiff"),
                "points": team.get("pts")
            }

    return teams_data


def generate_players_data(teams_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extrae jugadores reales de cada equipo"""
    all_players = []
    player_counter = 1

    for team_id_str, team_info in teams_data.items():
        team_id = int(team_id_str)
        team_name = team_info["name"]
        league = team_info["league"]

        print(f"  Obteniendo jugadores de {team_name}...")
        players = fetch_players(team_id, team_name)

        for player in players:
            all_players.append({
                "id": player_counter,
                "name": player.get("name"),
                "position": player.get("position"),
                "age": player.get("age"),
                "nationality": player.get("nationality"),
                "rating": player.get("rating"),
                "goals": player.get("goals", 0),
                "assists": player.get("assists", 0),
                "team_id": team_id,
                "team_name": team_name,
                "league": league
            })
            player_counter += 1

        # Pequeña pausa para no saturar la API
        time.sleep(0.5)

    return all_players


def generate_tactical_data(teams_data: Dict[str, Any]) -> Dict[str, Any]:
    """Genera información táctica para cada equipo"""
    tactical_data = {}
    formations = TACTICAL_INFO["formations"]
    playstyles = TACTICAL_INFO["playstyles"]

    for idx, (team_id_str, team_info) in enumerate(teams_data.items()):
        position = team_info["position"]
        goals_for = team_info.get("goals_for") or 0
        goals_against = team_info.get("goals_against") or 0
        wins = team_info.get("wins") or 0
        losses = team_info.get("losses") or 0

        if position <= 2:
            formation = formations[0]
            playstyle = playstyles[0]
        elif position == 3:
            formation = formations[1]
            playstyle = playstyles[1]
        else:
            formation = formations[3]
            playstyle = playstyles[2]

        characteristics = []
        if goals_for > 15:
            characteristics.append("Ataque fluido")
        if goals_against < 10:
            characteristics.append("Defensa sólida")
        if position == 1:
            characteristics.append("Líderes actuales")
        if wins > losses:
            characteristics.append("Consistentes")
        if not characteristics:
            characteristics = ["Juego equilibrado"]

        tactical_data[team_id_str] = {
            "team_id": int(team_id_str),
            "team_name": team_info["name"],
            "league": team_info["league"],
            "formation": formation,
            "playstyle": playstyle,
            "characteristics": characteristics,
            "strengths": ["Juego coordinado", "Transiciones rápidas"],
            "weaknesses": ["Inconsistencia en momentos clave", "Vulnerabilidad a presión alta"]
        }

    return tactical_data


def save_json(data: Any, filepath: Path) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Guardado: {filepath}")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    print("\n🚀 Iniciando extracción de datos con Free API Live Football...\n")

    # Paso 1: Standings
    print("📊 Extrayendo standings...")
    all_standings = {}
    for league_name, league_id in LEAGUE_IDS.items():
        standings = fetch_standings(league_name, league_id)
        all_standings[league_name] = standings
        time.sleep(0.5)

    # Paso 2: Equipos
    print("\n👥 Generando datos de equipos...")
    teams_data = generate_teams_data(all_standings)
    print(f"✅ {len(teams_data)} equipos generados")

    # Paso 3: Jugadores reales
    print("\n⚽ Obteniendo jugadores reales...")
    players_data = generate_players_data(teams_data)
    print(f"✅ {len(players_data)} jugadores obtenidos")

    # Paso 4: Táctica
    print("\n🎯 Generando información táctica...")
    tactical_data = generate_tactical_data(teams_data)
    print(f"✅ {len(tactical_data)} perfiles tácticos generados")

    # Paso 5: Guardar
    print("\n💾 Guardando archivos JSON...")
    save_json(teams_data, TEAMS_OUTPUT)
    save_json(players_data, PLAYERS_OUTPUT)
    save_json(tactical_data, TACTICAL_OUTPUT)

    print("\n✨ ¡Ingesta completada!")
    print(f"📁 Archivos en: {DATA_DIR}/")


if __name__ == "__main__":
    main()