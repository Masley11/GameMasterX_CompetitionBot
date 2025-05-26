import requests
import mysql.connector
from datetime import datetime
import os

API_TOKEN = os.getenv("PANDASCORE_TOKEN")
GAMES = ["cs-go", "dota-2", "league-of-legends"]

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME
)
cursor = conn.cursor()

for game in GAMES:
    url = f"https://api.pandascore.co/{game}/matches?token={API_TOKEN}&sort=-begin_at&per_page=5"
    res = requests.get(url)
    if res.status_code != 200:
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

        cursor.execute("""
            INSERT INTO results (game_name, team1, team2, score1, score2, match_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE score1 = VALUES(score1), score2 = VALUES(score2)
        """, (game.upper(), team1, team2, score1, score2, match_date))

conn.commit()
conn.close()
