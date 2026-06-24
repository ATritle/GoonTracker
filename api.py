from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

import sqlite3

app = FastAPI(
    title="Goon Tracker API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "data/sightings.db"


@app.get("/")
def root():

    return {
        "status": "online",
        "service": "Goon Tracker API"
    }


@app.get("/current_status")
def current_status():

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            source,
            map,
            game_mode,
            report_time,
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

    reports = []

    for row in rows:

        reports.append(
            {
                "source": row[0],
                "map": row[1],
                "game_mode": row[2],
                "report_time": row[3],
                "collected_at": row[4]
            }
        )

    unique_maps = {
        report["map"]
        for report in reports
    }

    status = (
        "AGREEMENT"
        if len(unique_maps) == 1
        else "DISAGREEMENT"
    )

    return {
        "status": status,
        "reports": reports
    }


@app.get("/history")
def history():

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            source,
            map,
            game_mode,
            report_time,
            collected_at
        FROM sightings
        ORDER BY id DESC
        LIMIT 100
    """)

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "source": row[0],
            "map": row[1],
            "game_mode": row[2],
            "report_time": row[3],
            "collected_at": row[4]
        }
        for row in rows
    ]


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
