import sqlite3
from collections import Counter

from fastapi import FastAPI

app = FastAPI(
    title="Goon Tracker API",
    version="1.0.0"
)

DB_FILE = "data/sightings.db"


@app.get("/")
def root():

    return {
        "status": "online",
        "service": "Goon Tracker API"
    }


@app.get("/current")
def current():

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            source,
            map,
            collected_at
        FROM sightings
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "source": row[0],
            "map": row[1],
            "collected_at": row[2]
        }
        for row in rows
    ]


@app.get("/consensus")
def consensus():

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            source,
            map,
            collected_at
        FROM sightings
        WHERE id IN (
            SELECT MAX(id)
            FROM sightings
            GROUP BY source
        )
    """)

    rows = cursor.fetchall()

    conn.close()

    if not rows:

        return {
            "map": None,
            "confidence": 0,
            "sources": 0
        }

    maps = [row[1] for row in rows]

    counts = Counter(maps)

    current_map = counts.most_common(1)[0][0]

    confidence = (
        counts[current_map]
        / len(maps)
    ) * 100

    return {
        "map": current_map,
        "confidence": round(confidence, 2),
        "sources": len(rows),
        "tracker_results": [
            {
                "source": row[0],
                "map": row[1],
                "collected_at": row[2]
            }
            for row in rows
        ]
    }


@app.get("/stats")
def stats():

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            map,
            COUNT(*)
        FROM sightings
        GROUP BY map
        ORDER BY COUNT(*) DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "map": row[0],
            "count": row[1]
        }
        for row in rows
    ]
