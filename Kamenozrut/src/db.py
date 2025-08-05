import sqlite3

conn = sqlite3.connect("game_scores.db")

cursor = conn.cursor()

# TODO timestamp is in UTC - i need to get the time of the PC
cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    musiclevel INTEGER,
    soundlevel INTEGER,
    colorscheme INTEGER
)
""")


def set_score(score):
    cursor.execute("INSERT INTO scores (score) VALUES (?)", (score,))
    conn.commit()


def get_max_score():
    cursor.execute("SELECT score FROM scores ORDER BY score DESC LIMIT 1")
    return cursor.fetchone()[0]


def set_musiclevel(musiclevel):
    cursor.execute("UPDATE settings SET musiclevel = ? WHERE id = 1", (musiclevel,))
    conn.commit()


def get_musiclevel():
    cursor.execute("SELECT musiclevel FROM settings")
    return cursor.fetchone()[0]


def set_soundlevel(soundlevel):
    cursor.execute("UPDATE settings SET soundlevel = ? WHERE id = 1", (soundlevel,))
    conn.commit()


def get_soundlevel():
    cursor.execute("SELECT soundlevel FROM settings")
    return cursor.fetchone()[0]


def set_colorscheme(colorscheme):
    cursor.execute("UPDATE settings SET colorscheme = ? WHERE id = 1", (colorscheme,))
    conn.commit()


def get_colorscheme():
    cursor.execute("SELECT colorscheme FROM settings")
    return cursor.fetchone()[0]
