import sqlite3

conn = sqlite3.connect("game_scores.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

def save_score(score):
    cursor.execute("INSERT INTO scores (score) VALUES (?)", (score,))
    conn.commit()
