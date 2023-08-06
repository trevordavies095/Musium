import argparse
import logging
import yaml
from db_layer import DbLayer
from math import floor
from music_brainz import MusicBrainz
from prettytable import PrettyTable


def main():
    config = load_config()
    args = term_args()
    mb = MusicBrainz()
    db = DbLayer(config)

    # Check to see if we are doing a report
    if args.artist or args.album or args.year or args.decade or args.all_time or args.top_artists:
        
        #q[0] - is the type of report
        #q[1] - is the query to run to get the report
        q = parse_query(args, args.top_artists)
        if q is None:
            print("Incorrect query format")
            exit(1)
        
        results = db.run_query(q[1])
        
        score = 0
        if args.artist:
            for r in results:
                score += r[3]
            if len(results) > 0:
                score /= len(results)
        
                if args.top_artists:
                    output_report([q[0], results, args.top_artists])
                else:
                    output_report([q[0], results, score])
            else:
                print("Not found!")
            exit(0)

    # Check to see if exporting csv
    if args.export_csv:
        db.export_csv()
        exit(0)

    # Check to see if musicbrainz ID was passed in
    if args.mb_id:
        r = db.search_mb(mb_id=args.mb_id)

        # If not found in DB, grab from MB
        if r is not None:
            print("Found album in DB!")

        r = mb.Search(artist=None, album=None, year=None, mb_id=args.mb_id)

    # Manual search
    else:
        artist = input("Artist > ")
        album = input("Album > ")
        year = input("Year > ")

        # Check to see if release already in DB
        r = db.search(artist, album, year)
    
        # If not found in DB, search MB for it
        if r is None:
            r = mb.Search(artist, album, year)
        else:
            print("Found album in DB!")
            r = mb.Search(artist, album, year, r[0])
    
    # Verify the search results are correct 
    correct = check_details(r)
    if args.mb_id and correct != "c":
        exit(0)        

    # If the results are incorrect, prompt the user for the correct Musicbrainz ID
    if correct != "c":
        mb_id = input("Enter ID: ")
        r = mb.Search(artist, album, year, mb_id)
        c = check_details(r)
        if r is None: exit

        if c != "c":
            exit(0)

    rate_album(config, r)

    
def rate_album(config, r):
    
    total = 0
    for track in r.track_list:
        track[2] = float(input(track[0] + ". " + track[1] + " score: "))
        total += track[2]

    score = floor(((total / len(r.track_list)*10) + config["bonus"]) * 10)
    star_rating = score / 20

    if score >= 100: score = 100
    r.rating = score

    star_rating = round(star_rating * 2) / 2
    r.star_rating = star_rating

    print("-------------------------------------------")
    print("Score: " + str(score))
    print("Stars: " + str(star_rating))
    db = DbLayer(config)
    db.rate_album(r)

def check_details(r):
    print()
    print("Artist: " + r.artist)
    print("Album: " + r.album + " (" + str(r.year) + ")")
    print("-------------------------------------------")
    for track in r.track_list:
        print(track[0] + ". " + track[1])

    print()

    return input('\033[34m' + '[C]' + '\033[39m' + 'orrect? ').lower().strip()


def term_args():
    """
    Inputs commands from the console, parses
    them, then returns them to main.
    :return: The parsed args
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-mb", "--mb_id", type=str, help="Music Brainz ID of release to be scored")
    parser.add_argument("-ar", "--artist", help="Artist to be used in query")
    parser.add_argument("-al", "--album", help="Album to be used in query")
    parser.add_argument("-y", "--year", help="Year to be used in query")
    parser.add_argument("-d", "--decade", help="Decade to be used in query")
    parser.add_argument("-at", "--all_time", help="Returns your rated albums in DESC order", action='store_true')
    parser.add_argument("-ta", "--top_artists", help="Top artist based on average album score", type=int, nargs='?', const=5)
    parser.add_argument("-ex", "--export_csv", help="Export Musium.db to a CSV file", action='store_true')

    return parser.parse_args()


def load_config():
        try:
            stream = open("config.yaml", "r")
            config = yaml.safe_load(stream)

        except FileNotFoundError:
            print("Missing config.yaml!")
            exit(1)

        return config


def parse_query(args, min):

    # IF artist and album
    if args.artist and args.album:
        s_artist_album_sql = '''
            SELECT ar.name, al.name, al.year, al.rating, al.star_rating, t.name, t.track_score, al.musicbrainz_id FROM track t
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

    if args.top_artists:
        s_top_artists_sql = '''
            SELECT ar.name, round(avg(al.rating), 2) FROM album al
            INNER JOIN artist ar ON ar.id = al.artist_id
            GROUP BY ar.name
            HAVING COUNT(*) >= {}
            ORDER BY avg(al.rating) DESC;
        '''.format(str(min))

        return["top_artists", s_top_artists_sql, str(min)]


def output_report(r):
    artist_album_heading = ["Track", "Rating"]
    top_artists_heading = ["Artist", "Rating"]
    generic_heading = ["Artist", "Album", "Year", "Rating", "Stars"]

    report_type = r[0]
    report = r[1]

    if report_type == "artist_album": 
        print(report[0][0] + " - " + report[0][1] + " (" + str(report[0][2]) + ")")
        print("MusicBrainz ID: {}".format(str(report[0][7])))
        output_table = PrettyTable(artist_album_heading)
        for row in report:
            output_table.add_row([row[5], row[6]])
        print(output_table)

        print("Rating: {}, {} stars".format(report[0][3], report[0][4]))
    elif report_type == "artist":
        print("Average Artist Rating: " + str(round(r[2], 2)))
        output_table = PrettyTable(generic_heading)
        output_table.add_rows(report)
        print(output_table)
    elif report_type == "top_artists":
        print("Minimum Albums: {}".format(r[2]))
        output_table = PrettyTable(top_artists_heading)
        output_table.add_rows(report)
        print(output_table)
    else:
        output_table = PrettyTable(generic_heading)
        output_table.add_rows(report)
        print(output_table)



class ReleaseObj(object):
    musicbrainz_release_id = ""
    artist = ""
    album = ""
    year = ""
    track_list = []                         # i0 - track number, i1 - track name, i2 - track score
    rating = 0
    star_rating = 0

    def __init__(self, musicbrainz_release_id, artist, album, year, track_list):
        self.musicbrainz_release_id = musicbrainz_release_id
        self.artist = artist
        self.album = album
        self.year = year
        self.track_list = track_list


    def __str__(self):
        return "\n".join((self.musicbrainz_release_id, self.artist, self.album, str(self.year)))


if __name__ == "__main__":
    main()
