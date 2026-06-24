import sqlite3

conn = sqlite3.connect("data/sightings.db")

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

print("\nMOST COMMON MAPS\n")

for row in rows:
    print(
        f"{row[0]:<15} {row[1]}"
    )

conn.close()
