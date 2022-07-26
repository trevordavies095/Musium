from datetime import datetime
import musicbrainzngs as mb

class MusicBrainz:
    def __init__(self):
        mb.set_useragent("Musium", "0.1", "https://github.com/trevordavies095/Musium")

    def Search(self, artist, album, year, mb_id=None):
        #r = mb.search_release_groups(" ".join([artist, album, year]))["release-group-list"]
        #ids = [val['id'] for val in r]

        if mb_id is None:
            r = mb.search_releases(artist=artist, release=album, limit=5)['release-list']
            
            for x in r:
                try:
                    mb_id = x['id']
                    artist = x['artist-credit'][0]['name']
                    album = x['title']
                    year = datetime.strptime(x['date'], "%Y-%m-%d").year
                except:
                    continue

            if r is None: return None

        else:
            r = mb.get_release_by_id(id=mb_id, includes=["recordings", "artists"])['release']

            mb_id = r['id']
            artist = r['artist-credit'][0]['artist']['name']
            album = r['title']
            try:
                year = datetime.strptime(r['date'], "%Y-%m-%d").year
            except:
                year = r['date']

            if r is None: return None

            
        track_list = self.get_track_list(mb_id)
        if track_list is None: return None

        return ReleaseObj(mb_id, artist, album, year, track_list)

    def get_track_list(self, mb_id):
        track_list = []
        r = mb.get_release_by_id(id=mb_id, includes=["recordings"])["release"]["medium-list"]

        # Looping in case this is a double album
        for medium in r:
            tl = medium["track-list"]

            for x in range(len(tl)):
                line = (tl[x])
                track_list.append([line["number"], line["recording"]["title"], -1])
        
        return track_list


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

