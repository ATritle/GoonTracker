import sqlite3

DB_FILE = "data/sightings.db"


def initialize():

    conn = sqlite3.connect(DB_FILE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS sightings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            map TEXT NOT NULL,
            game_mode TEXT,
            report_time TEXT,
            collected_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_sighting(source, map_name):

    conn = sqlite3.connect(DB_FILE)

    conn.execute(
        """
        INSERT INTO sightings (
            source,
            map
        )
        VALUES (?, ?)
        """,
        (source, map_name)
    )

    conn.commit()
    conn.close()


def get_latest_map(source):

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT map
        FROM sightings
        WHERE source = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (source,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None
