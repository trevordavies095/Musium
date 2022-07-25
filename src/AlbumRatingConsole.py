from colorama import Fore
from DbLayer import DbLayer
from MusicBrainz import MusicBrainz

def main():
    mb = MusicBrainz()

    #artist = input("Artist > ")
    #album = input("Album > ")
    #year = input("Year > ")

    r = mb.Search("Radiohead", "A Moon Shaped Pool", "2016")
    correct = CheckDetails(r)

    if correct != "c":
        mb_id = input("Enter ID: ")
        r = mb.Search("Radiohead", "A Moon Shaped Pool", "2016")
        c = CheckDetails(r)
        if r is None: exit

        if c != "c":
            exit


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