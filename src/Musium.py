from db_layer import DbLayer
from math import floor
from music_brainz import MusicBrainz
from query_parse import parse_query
from reporting import output_report
import argparse
import yaml

def main():
    config = load_config()
    args = term_args()
    mb = MusicBrainz()
    db = DbLayer(config)

    if args.artist or args.album or args.year or args.decade or args.all_time:
        q = parse_query(args)
        if q is None:
            print("Incorrect query format")
            exit(1)
        results = db.run_query(q[1])
        output_report([q[0], results])
        exit(0)

    if args.mb_id:
        r = mb.Search(artist=None, album=None, year=None, mb_id=args.mb_id)

    else:
        artist = input("Artist > ")
        album = input("Album > ")
        year = input("Year > ")

        r = db.search(artist, album, year)
    
        if r is None:
            r = mb.Search(artist, album, year)
        else:
            print("Found album in DB!")
            r = mb.Search(artist, album, year, r[0])
    correct = check_details(r)

    if correct != "c":
        mb_id = input("Enter ID: ")
        r = mb.Search(artist, album, year, mb_id)
        c = check_details(r)
        if r is None: exit

        if c != "c":
            exit

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

    return parser.parse_args()


def load_config():
        try:
            stream = open("config.yaml", "r")
            config = yaml.load(stream)

        except FileNotFoundError:
            print("Missing config.yaml!")
            exit(1)

        return config


if __name__ == "__main__":
    main()
