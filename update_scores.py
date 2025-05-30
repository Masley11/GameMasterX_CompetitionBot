import requests
import os
from datetime import datetime

# === CONFIGURATION ===
API_TOKEN = os.getenv("PANDASCORE_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

GAMES = ["cs-go", "dota-2", "league-of-legends"]

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

for game in GAMES:
    url = f"https://api.pandascore.co/{game}/matches?token={API_TOKEN}&sort=-begin_at&per_page=5"
    res = requests.get(url)
    if res.status_code != 200:
        print(f"Erreur API PandaScore pour {game}: {res.status_code}")
        continue

    data = res.json()

    for match in data:
        if not match["opponents"] or len(match["opponents"]) < 2:
            continue
        team1 = match["opponents"][0]["opponent"]["name"]
        team2 = match["opponents"][1]["opponent"]["name"]
        score1 = match["results"][0]["score"] if match["results"] else 0
        score2 = match["results"][1]["score"] if len(match["results"]) > 1 else 0
        date = match["begin_at"] or match["scheduled_at"]
        match_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

        status = match["status"]  # Ex: "finished", "running", etc.
        if status == "running":
            status = "live"
        elif status == "not_started":
            status = "scheduled"

        payload = {
            "game_name": game.upper(),
            "team_a": team1,
            "team_b": team2,
            "score_a": score1,
            "score_b": score2,
            "match_date": match_date.isoformat(),
            "status": status
        }

        response = requests.post(f"{SUPABASE_URL}/rest/v1/match_results", headers=headers, json=payload)
        if response.status_code not in [200, 201, 204]:
            print("❌ Échec :", response.status_code, response.text)
        else:
            print(f"✅ Match ajouté : {team1} vs {team2}")
