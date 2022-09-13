def parse_query(args):

    # IF artist and album
    if args.artist and args.album:
        s_artist_album_sql = '''
            SELECT ar.name, al.name, al.year, al.rating, al.star_rating, t.name, t.track_score FROM track t
            INNER JOIN album al ON al.id = t.album_id 
            INNER JOIN artist ar ON ar.id = al.artist_id
            WHERE ar.name = "{}" COLLATE NOCASE
            AND al.name = "{}" COLLATE NOCASE
            ORDER BY t.id ASC;
        '''
        return ["artist_album", s_artist_album_sql.format(args.artist, args.album)]

    # IF artist
    if args.artist:
        s_artist_sql = '''
            SELECT ar.name, al.name, al.year, al.rating, al.star_rating FROM album al
            INNER JOIN artist ar ON ar.id = al.artist_id
            WHERE ar.name = "{}" COLLATE NOCASE
            ORDER BY al.year ASC;
        '''
        return ["artist", s_artist_sql.format(args.artist)]

    # IF year
    if args.year:
        s_year_sql = '''
            SELECT ar.name, al.name, al.year, al.rating, al.star_rating FROM album al
            INNER JOIN artist ar ON ar.id = al.artist_id
            WHERE al.year = {}
            ORDER BY al.rating DESC;
        '''
        return ["year", s_year_sql.format(args.year)]

    # IF decade
    if args.decade:
        low = int(args.decade.split("s")[0])
        high = low + 9

        s_decade_sql = '''
            SELECT ar.name, al.name, al.year, al.rating, al.star_rating FROM album al
            INNER JOIN artist ar ON ar.id = al.artist_id
            WHERE al.year BETWEEN {} AND {}
            ORDER BY al.rating DESC;
        '''
        
        return ["decade", s_decade_sql.format(str(low), str(high))]

    if args.all_time:
        s_all_time_sql = '''
            SELECT ar.name, al.name, al.year, al.rating, al.star_rating FROM album al
            INNER JOIN artist ar ON ar.id = al.artist_id
            ORDER BY al.rating DESC;
        '''

        return["all_time", s_all_time_sql]
