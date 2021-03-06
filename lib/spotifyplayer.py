from __future__ import unicode_literals

import sys
import copy
import threading
import json
import spotify
import spotipy
import random
from spotify import utils
from spotipy.oauth2 import SpotifyClientCredentials

class Song:
    def __init__(self, uri, title, artist, duration):
        self.uri = uri
        self.title = title
        self.artist = artist
        self.duration = duration

    @property
    def duration_readable(self):
        seconds = int((self.duration / 1000) % 60)
        minutes = int(self.duration / 1000 / 60)
        return "%d:%02d" %(minutes, seconds)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"{0} - {1} ({2})".format(self.artist, self.title, self.duration_readable)

    def __eq__(self, other):
        if not isinstance(other, Song):
            return False
        return self.uri == other.uri

class SpotifyPlayer(utils.EventEmitter):
    PLAY_TRACK = "player_new_track"
    PLAY_PLAY = "player_track_play"
    PLAY_PAUSE = "player_track_pause"
    PLAY_STOP = "player_track_stop"
    PLAY_END = "player_track_done"
    MODE = "player"
    def __init__(self, settings):
        # Initialize the EventEmitter
        super(SpotifyPlayer, self).__init__()
        self.session = None

        client_credentials_manager = SpotifyClientCredentials()
        self.web = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        # Events for coordination
        self._logged_in = threading.Event()
        self._loop =  None
        self._search_history = {}
        self._settings = settings
        self.current = None
        self.playing = False
        self.mode = None
        self.login()
        self.history_length = 10
        self.history = []

    def login(self):
        # Assuming a spotify_appkey.key in the current dir
        self.session = spotify.Session()

        # Process events in the background
        self._loop = spotify.EventLoop(self.session)
        self._loop.start()

        # Connect an audio sink
        if sys.platform == "darwin":
            audio = spotify.PortAudioSink(self.session)
        else:
            audio = spotify.AlsaSink(self.session)

        # Register event listeners
        self.session.on(
            spotify.SessionEvent.CONNECTION_STATE_UPDATED, self._on_connection_state_updated)
        self.session.on(spotify.SessionEvent.END_OF_TRACK, self._on_end_of_track)

        # Assuming a previous login with remember_me=True and a proper logout
        if self._settings.SPOTIFY_USERNAME == None or self._settings.SPOTIFY_PASSWORD == None:
            raise StandardError("No username/password")
        self.session.login(self._settings.SPOTIFY_USERNAME,self._settings.SPOTIFY_PASSWORD)

        self._logged_in.wait()
        return self.session

    def logout(self):
        self.session.logout()
        self.session = None

    def play(self, song, mode=None):
        if mode == None:
            self.mode = self.MODE
        else:
            self.mode = mode
        # Play a track
        self.current = song

        # Add to history
        self.history.insert(0, song)
        if len(self.history) > self.history_length:
            self.history = self.history[0:self.history_length]

        self.session.player.unload()
        self.emit(self.PLAY_TRACK, self.current)
        trackdata = self.session.get_track(song.uri).load()
        self.session.player.load(trackdata)
        self.session.player.play()
        self.playing = True
        return song

    def related(self, song=None, user=None, single=False, artist_limit = 5, song_limit=5):
        # Use the current song if no song is supplied
        if not song:
            song = self.current
        # Use the history if no song is supplied
        if not song and len(self.history) > 0:
            song = self.history[0]
        if not song:
            return None
        track = self.web.track(song.uri)
        artist = track['artists'][0]['id']
        rel_artists = self.web.artist_related_artists(artist)

        top_artists = sorted(rel_artists['artists'],key=lambda a: a['popularity'], reverse=True)

        if len(top_artists) == 0:
            return None
        # Pick a random related artists
        if single:
            top_artists = [random.choice(top_artists)]
            song_limit = 99 #increase the limit to allow for a more random pick
        else:
            top_artists = top_artists[0:artist_limit]

        top_tracks = map(
            lambda a:
                sorted(
                    self.web.artist_top_tracks(
                            a['id'],
                            country=self._settings.SPOTIFY_MARKET
                        )['tracks'],
                    key=lambda a: a['popularity'],
                    reverse=True
                )[0:song_limit],
            top_artists
        )
        flat_top_tracks = [item for sublist in top_tracks for item in sublist]

        # Convert to song objects
        result = map(
            self._convert_search,
            flat_top_tracks)

        if len(result) == 0:
            return None

        if not user == None:
            self._search_history[user] = result

        if single:
            return random.choice(result)

        return result


    def playpause(self):
        self.playing = not self.playing
        if self.playing:
            self.emit(self.PLAY_PLAY, self.current)
        else:
            self.emit(self.PLAY_PAUSE, self.current)
        self.session.player.play(self.playing)

    def stop(self):
        self.emit(self.PLAY_STOP, self.current)
        self.session.player.unload()
        self.playing = False
        self.current = None

    def search(self, query, user=None):
        search = self.web._get('search', q=query, limit=25, type="track",market=self._settings.SPOTIFY_MARKET)
        result = map(
            self._convert_search,
            filter(
                lambda x: self._settings.SPOTIFY_MARKET in x['available_markets'],
                search['tracks']['items']))
        if not user == None:
            self._search_history[user] = result
        return result

    def search_history(self, user, index):
        if user in self._search_history:
            result = self._search_history[user]
            if index < len(result):
                return result[index]
        return None

    def _convert_search(self, result):
        return Song(
            result['uri'],
            result['name'],
            ', '.join(map(lambda a: a['name'], result['artists'])),
            int(result['duration_ms']))

    def _on_end_of_track(self, data):
        current = self.current
        if self.current != None:
            self.mode = None
            self.playing = False
            self.current = None
            self.session.player.unload()
            self.emit(self.PLAY_END, current)

    def _on_connection_state_updated(self, session):
        if self.session.connection.state is spotify.ConnectionState.LOGGED_IN:
            self._logged_in.set()
