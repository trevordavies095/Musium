from datetime import datetime

from matplotlib import artist
from ReleaseObj import ReleaseObj
import musicbrainzngs as mb

class MusicBrainz:
    def __init__(self):
        mb.set_useragent("AlbumRating-Console", "0.1", "https://github.com/trevordavies095/AlbumRating")

    def Search(self, artist, album, year, mb_id=None):
        #r = mb.search_release_groups(" ".join([artist, album, year]))["release-group-list"]
        #ids = [val['id'] for val in r]

        if mb_id is None:
            r = mb.search_releases(artist=artist, release=album, limit=1, format='Digital Media')['release-list'][0]
            if r is None: return None

            mb_id = r['id']
            artist = r['artist-credit'][0]['name']
            album = r['title']
            year = datetime.strptime(r['date'], "%Y-%m-%d").year
            
        track_list = self.GetTrackList(mb_id)
        if track_list is None: return None
        
        return ReleaseObj(mb_id, artist, album, year, track_list)

    def GetTrackList(self, mb_id):
        track_list = []

        r = mb.get_release_by_id(id=mb_id, includes=["recordings"])
        tl = (r["release"]["medium-list"][0]["track-list"])

        for x in range(len(tl)):
            line = (tl[x])
            track_list.append((line["number"], line["recording"]["title"]))
        
        return track_list



    def test(self):
        # Returns dict with 'recording-list' key
        r = mb.search_release_groups("Radiohead The King of Limbs 2011")["release-group-list"]
        ids = [val['id'] for val in r]
        print(ids)

