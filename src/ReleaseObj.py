from numpy import arange


class ReleaseObj(object):
    musicbrainz_release_id = ""
    artist = ""
    album = ""
    year = ""
    track_list = []

    def __init__(self, musicbrainz_release_id, artist, album, year, track_list):
        self.musicbrainz_release_id = musicbrainz_release_id
        self.artist = artist
        self.album = album
        self.year = year
        self.track_list = track_list


    def __str__(self):
        return "\n".join((self.musicbrainz_release_id, self.artist, self.album, str(self.year)))
    