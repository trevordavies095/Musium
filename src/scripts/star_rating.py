import sqlite3

conn = sqlite3.connect("Musium-Backup.db")
c = conn.cursor()

s_score_sql = """
SELECT id, rating FROM album;
"""

c.execute(s_score_sql)
r = c.fetchall()
star_ratings = {}

for score in r:
    a_id = score[0]
    a_score = score[1] / 20
    star_score = round(a_score * 2) / 2
    star_ratings[a_id] = star_score

for key, value in star_ratings.items():
    u = """
        UPDATE album
        SET star_rating = {}
        WHERE id = {};
    """.format(value, key)
    c.execute(u)
conn.commit()