import sqlite3


class DbLayer:
    
    conn = None

    def __init__(self, config):
        try:
            self.conn = sqlite3.connect(config["dbpath"])
            c = self.conn.cursor()

            c_album_table_sql = '''
                CREATE TABLE "album" (
                    "id"	INTEGER NOT NULL,
                    "artist_id"	INTEGER NOT NULL,
                    "name"	TEXT NOT NULL,
                    "year"	INTEGER NOT NULL,
                    "rating"	INTEGER,
                    "musicbrainz_id"	TEXT,
                    "star_rating"	REAL,
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
            '''
            c.execute(c_album_table_sql)

            c_artist_table_sql = '''
                CREATE TABLE IF NOT EXISTS "artist" (
                    "id"	INTEGER NOT NULL,
                    "name"	TEXT NOT NULL UNIQUE,
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
            '''
            c.execute(c_artist_table_sql)

            c_track_table_sql = '''
                CREATE TABLE IF NOT EXISTS "track" (
                    "id"	INTEGER NOT NULL,
                    "album_id"	INTEGER NOT NULL,
                    "name"	TEXT NOT NULL,
                    "track_score"	INTEGER,
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
            '''
            c.execute(c_track_table_sql)

            self.conn.commit()

            print("DB created")



        except Exception as e:
            pass

    
    def search(self, artist, album, year):
        c = self.conn.cursor()

        check_album_sql = '''
            SELECT musicbrainz_id FROM album a
            INNER JOIN artist ar ON ar.id = a.artist_id
            WHERE ar.name = ? AND a.name = ? AND a.year = ?;
        '''
        c.execute(check_album_sql, (artist, album, year,))
        mb_id = c.fetchone()

        return mb_id
    
    def search_mb(self, mb_id):
        c = self.conn.cursor()

        check_mb_id_sql = '''
            SELECT musicbrainz_id FROM album WHERE musicbrainz_id = ?;
        '''
        c.execute(check_mb_id_sql, (mb_id,))
        exists = c.fetchone()

        return exists


    def run_query(self, q):
        c = self.conn.cursor()
        c.execute(q)
        return c.fetchall()

    def rate_album(self, r):
        c = self.conn.cursor()

        # Check to see if artist exists
        check_artist_sql = '''
            SELECT id FROM artist WHERE name = ?;
        '''
        c.execute(check_artist_sql, (r.artist,))   

        artist_id = c.fetchone()

        # If not add to db
        if artist_id is None:
            i_artist_sql = '''
                INSERT INTO artist(name)
                VALUES(?)
            '''

            c.execute(i_artist_sql, (r.artist,))
            self.conn.commit()
            artist_id = c.lastrowid
        else:
            artist_id = artist_id[0]

        
        # Check to see if album exists
        check_album_sql = '''
            SELECT id FROM album WHERE artist_id = ? AND name = ? AND year = ?;
        '''
        c.execute(check_album_sql, (artist_id, r.album, r.year,))

        album_id = c.fetchone()
    
        # If not add to db
        if album_id is None:
            i_album_sql = '''
                INSERT INTO album(artist_id, name, year, rating, musicbrainz_id, star_rating)
                VALUES (?, ?, ?, ?, ?, ?);
            '''

            c.execute(i_album_sql, (artist_id, r.album, r.year, r.rating, r.musicbrainz_release_id, r.star_rating))
            self.conn.commit()
            album_id = c.lastrowid

        else:
            album_id = album_id[0]
            u_album_sql = '''
                UPDATE album
                SET rating = ?, star_rating = ?
                WHERE id = ?;
            '''
            c.execute(u_album_sql, (r.rating, r.star_rating, album_id,))

        for track in r.track_list:
            # Check to see if track exists
            check_track_sql = '''
                SELECT id FROM track WHERE album_id = ? AND name = ?;
            '''
            c.execute(check_track_sql, (album_id, track[1],))
            track_id = c.fetchone()

            # If not add to db
            if track_id is None:
                i_track_sql = '''
                    INSERT INTO track(album_id, name, track_score)
                    VALUES (?, ?, ?);
                '''

                c.execute(i_track_sql, (album_id, track[1], track[2],))
                self.conn.commit()
                track_id = c.lastrowid
            
            # Else update track rating
            else:
                track_id = track_id[0]
                u_track_sql = '''
                    UPDATE track
                    SET track_score = ?
                    WHERE id = ?;
                '''
                c.execute(u_track_sql, (track[2], track_id))
                self.conn.commit()


