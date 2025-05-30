import requests
import yaml

# === CONFIGURATION ===
SUPABASE_URL = "https://ajtzkuhsnymajitgdlaw.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFqdHprdWhzbnltYWppdGdkbGF3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg2Mzc1NzYsImV4cCI6MjA2NDIxMzU3Nn0.39b3yt9ci8Ulq2uP-MNoyQ_u1jcxVdwyiiM72zO4yZc"

# === LIRE LE FICHIER YAML ===
with open("scores.yml", "r") as f:
    matches = yaml.safe_load(f)

# === ENVOI VERS SUPABASE ===
url = f"{SUPABASE_URL}/rest/v1/match_results"
headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

for match in matches:
    response = requests.post(url, headers=headers, json=match)
    if response.status_code in [200, 201, 204]:
        print(f"✅ Match ajouté : {match['team_a']} vs {match['team_b']}")
    else:
        print(f"❌ Erreur pour le match : {match}")
        print(response.status_code, response.text)
