from datetime import datetime
from ReleaseObj import ReleaseObj
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

            
        track_list = self.GetTrackList(mb_id)
        if track_list is None: return None

        return ReleaseObj(mb_id, artist, album, year, track_list)

    def GetTrackList(self, mb_id):
        track_list = []
        r = mb.get_release_by_id(id=mb_id, includes=["recordings"])
        tl = (r["release"]["medium-list"][0]["track-list"])

        for x in range(len(tl)):
            line = (tl[x])
            track_list.append([line["number"], line["recording"]["title"], -1])
        
        return track_list



    def test(self):
        # Returns dict with 'recording-list' key
        r = mb.search_release_groups("Radiohead The King of Limbs 2011")["release-group-list"]
        ids = [val['id'] for val in r]
        print(ids)

