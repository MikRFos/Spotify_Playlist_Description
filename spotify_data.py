import spotipy
from spotipy import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials
from database import db, Song

PITCH_CLASS_CONVERSION = {
    0: "C",
    1: "C#",
    2: "D",
    3: "D#",
    4: "E",
    5: "F",
    6: "F#",
    7: "G",
    8: "G#",
    9: "A",
    10: "A#",
    11: "B"
}


class SpotifyPlaylist:
    def __init__(self, playlist):
        playlist_id = playlist.split("/")[-1]
        self._spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        try:
            self._playlist_full = self._spotify.playlist(playlist_id)
        except SpotifyException:
            raise SpotifyException

    def get_songs(self):
        song_list = []
        playlist_track_list = self._playlist_full["tracks"]["items"]
        for song in playlist_track_list:
            song = song["track"]
            song_title = song["name"]
            song_q = Song.query.filter_by(title=song_title).first()
            if bool(song_q):
                song_list.append(song_q.to_dict())
            else:
                song_artist = song["artists"][0]["name"]
                song_id = song["id"]
                song_length_s = int(song["duration_ms"]) / 1000
                song_length_m = int(song_length_s // 60)
                song_length_m_s = f"{song_length_m}:{round(song_length_s % 60)}"
                song_image_url = song["album"]["images"][0]["url"]
                song_data = self._spotify.audio_analysis(song_id)["track"]
                tempo = song_data["tempo"]
                mode = "Major" if song_data["mode"] == 1 else "Minor"
                key = PITCH_CLASS_CONVERSION[song_data["key"]]
                signature = f"{song_data['time_signature']}/4"
                new_song = Song(title=song_title, artist=song_artist, duration=song_length_m_s,
                                tempo=tempo, key=f"{key} {mode}", signature=signature,
                                image_url=song_image_url, song_id=song_id)
                db.session.add(new_song)
                db.session.commit()
                song_list.append(new_song)

        return song_list
