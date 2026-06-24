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


def save_sighting(
    source,
    map_name,
    game_mode=None,
    report_time=None
):

    conn = sqlite3.connect(DB_FILE)

    conn.execute(
        """
        INSERT INTO sightings (
            source,
            map,
            game_mode,
            report_time
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            source,
            map_name,
            game_mode,
            report_time
        )
    )

    conn.commit()
    conn.close()


def get_latest_sighting(source):

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            map,
            game_mode,
            report_time
        FROM sightings
        WHERE source = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (source,)
    )

    row = cursor.fetchone()

    conn.close()

    if not row:
        return None

    return {
        "map": row[0],
        "game_mode": row[1],
        "report_time": row[2]
    }
