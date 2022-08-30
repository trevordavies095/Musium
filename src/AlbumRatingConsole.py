from colorama import Fore
from DbLayer import DbLayer
from math import floor
from MusicBrainz import MusicBrainz

def main():
    mb = MusicBrainz()
    db = DbLayer()

    artist = input("Artist > ")
    album = input("Album > ")
    year = input("Year > ")

    r = db.Search(artist, album, year)
    if r is None:
        r = mb.Search(artist, album, year)
    else:
        print("Found album in DB!")
        r = mb.Search(artist, album, year, r[0])
    correct = CheckDetails(r)

    if correct != "c":
        mb_id = input("Enter ID: ")
        r = mb.Search(artist, album, year, mb_id)
        c = CheckDetails(r)
        if r is None: exit

        if c != "c":
            exit

    RateAlbum(r)

    
def RateAlbum(r):
    total = 0
    for track in r.track_list:
        track[2] = float(input(track[0] + ". " + track[1] + " score: "))
        total += track[2]

    score = floor(((total / len(r.track_list)*10) + .15) * 10)
    r.rating = score
    db = DbLayer()
    db.RateAlbum(r)

def CheckDetails(r):
    print()
    print("Artist: " + r.artist)
    print("Album: " + r.album + " (" + str(r.year) + ")")
    print("-------------------------------------------")
    for track in r.track_list:
        print(track[0] + ". " + track[1])

    print()

    return input('\033[34m' + '[C]' + '\033[39m' + 'orrect? ').lower().strip()


    




if __name__ == "__main__":
    main()