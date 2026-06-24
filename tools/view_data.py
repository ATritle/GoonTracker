import sqlite3

conn = sqlite3.connect("data/sightings.db")

cursor = conn.cursor()

cursor.execute("""
    SELECT *
    FROM sightings
    ORDER BY id DESC
    LIMIT 20
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
