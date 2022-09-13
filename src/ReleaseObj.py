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
    