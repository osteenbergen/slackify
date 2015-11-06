from __future__ import unicode_literals

import sys
import copy
import threading
import json
import spotify
from spotify import utils

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
        return "%s - %s (%s)" % (self.artist, self.title, self.duration_readable)

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
        # Events for coordination
        self._logged_in = threading.Event()
        self._loop =  None
        self._search_history = {}
        self._settings = settings
        self.current = None
        self.playing = False
        self.mode = None
        self.login()

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
        self.emit(self.PLAY_TRACK, self.current)
        trackdata = self.session.get_track(song.uri).load()
        self.session.player.load(trackdata)
        self.session.player.play()
        self.playing = True
        return song

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
        search = self.session.search(query)
        search.load()
        result = map(
            self._convert_search,
            filter(
                lambda x: x.availability == spotify.TrackAvailability.AVAILABLE,
                search.tracks))
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
            result.link.uri,
            result.name,
            result.artists[0].name,
            int(result.duration))

    def _on_end_of_track(self, data):
        current = self.current
        if self.current != None:
            self.mode = None
            self.playing = False
            self.current = None
            self.emit(self.PLAY_END, current)

    def _on_connection_state_updated(self, session):
        if self.session.connection.state is spotify.ConnectionState.LOGGED_IN:
            self._logged_in.set()
