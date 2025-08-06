import sqlite3
import datetime

conn = sqlite3.connect("game_scores.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS standard_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER NOT NULL,
    timestamp DATETIME
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS color_madness_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER NOT NULL,
    timestamp DATETIME
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


def set_score(score, mode):
    if mode == "Standard":
        cursor.execute("INSERT INTO standard_scores (score, timestamp) VALUES (?,?)",
                       (score, datetime.datetime.now()))
    elif mode == "ColorMadness":
        cursor.execute("INSERT INTO color_madness_scores (score, timestamp) VALUES (?,?)",
                       (score, datetime.datetime.now()))
    conn.commit()


def get_max_score(mode):
    if mode == "Standard":
        cursor.execute("SELECT score FROM standard_scores ORDER BY score DESC LIMIT 1")
    elif mode == "ColorMadness":
        cursor.execute("SELECT score FROM color_madness_scores ORDER BY score DESC LIMIT 1")
    result = cursor.fetchone()
    if result is None:
        return 0  # alebo None, podľa toho čo ti dáva väčší zmysel
    return result[0]


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


def update_score(new_score, mode):
    if mode == "Standard":
        cursor.execute("SELECT id FROM standard_scores ORDER BY id DESC LIMIT 1")
    elif mode == "ColorMadness":
        cursor.execute("SELECT id FROM color_madness_scores ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()

    if result:
        last_id = result[0]
        cursor.execute("UPDATE standard_scores SET score = ? WHERE id = ?", (new_score, last_id))
        conn.commit()
