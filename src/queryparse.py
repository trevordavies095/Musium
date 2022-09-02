def parse_query(args):

    # IF artist and album
    if args.artist and args.album:
        s_artist_album_sql = '''
            SELECT ar.name, al.name, al.year, al.rating, t.name, t.track_score FROM track t
            INNER JOIN album al ON al.id = t.album_id 
            INNER JOIN artist ar ON ar.id = al.artist_id
            WHERE ar.name = "?" AND al.name = "?"
            ORDER BY t.id ASC;
        '''
        return ["artist_album", s_artist_album_sql.replace("?", args.artist, 1).replace("?", args.album, 1)]

    # IF artist
    if args.artist:
        s_artist_sql = '''
            SELECT ar.name, al.name, al.year, al.rating FROM album al
            INNER JOIN artist ar ON ar.id = al.artist_id
            WHERE ar.name = "?"
            ORDER BY al.year ASC;
        '''
        return ["artist", s_artist_sql.replace("?", args.artist, 1)]

    # IF year
    if args.year:
        s_year_sql = '''
            SELECT ar.name, al.name, al.year, al.rating FROM album al
            INNER JOIN artist ar ON ar.id = al.artist_id
            WHERE al.year = ?
            ORDER BY al.rating DESC;
        '''
        return ["year", s_year_sql.replace("?", args.year)]

    # IF decade
    if args.decade:
        low = int(args.decade.split("s")[0])
        high = low + 9

        s_decade_sql = '''
            SELECT ar.name, al.name, al.year, al.rating FROM album al
            INNER JOIN artist ar ON ar.id = al.artist_id
            WHERE al.year BETWEEN ? AND ?
            ORDER BY al.rating DESC;
        '''
        
        return ["decade", s_decade_sql.replace("?", str(low), 1).replace("?", str(high), 1)]


