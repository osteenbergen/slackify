from __future__ import unicode_literals

import sys
import copy
import threading
import json
import spotify
from spotify import utils
import credentials

class Song:
    def __init__(self, uri, title, artist):
        self.uri = uri
        self.title = title
        self.artist = artist

    def __str__(self):
        return "%s - %s" % (self.artist, self.title)

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
    def __init__(self):
        # Initialize the EventEmitter
        super(SpotifyPlayer, self).__init__()
        self.session = None
        # Events for coordination
        self.__logged_in = threading.Event()
        self.__loop =  None
        self.current = None
        self.playing = False
        self.login()

    def login(self):
        # Assuming a spotify_appkey.key in the current dir
        self.session = spotify.Session()

        # Process events in the background
        self.__loop = spotify.EventLoop(self.session)
        self.__loop.start()

        # Connect an audio sink
        if sys.platform == "darwin":
            audio = spotify.PortAudioSink(self.session)
        else:
            audio = spotify.AlsaSink(self.session)

        # Register event listeners
        self.session.on(
            spotify.SessionEvent.CONNECTION_STATE_UPDATED, self.__on_connection_state_updated)
        self.session.on(spotify.SessionEvent.END_OF_TRACK, self.__on_end_of_track)

        # Assuming a previous login with remember_me=True and a proper logout
        if credentials.username == None or credentials.password == None:
            raise StandardError("No username/password")
        self.session.login(credentials.username,credentials.password)

        self.__logged_in.wait()
        return self.session

    def logout(self):
        self.session.logout()
        self.session = None

    def play(self, song):
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
        self.session.player.unload()
        self.emit(self.PLAY_STOP, self.current)
        self.playing = False
        self.current = None

    def search(self, query):
        search = self.session.search(query)
        search.load()
        return map(
            self.__convert_search,
            filter(
                lambda x: x.availability == spotify.TrackAvailability.AVAILABLE,
                search.tracks))

    def __convert_search(self, result):
        return Song(
            result.link.uri,
            result.name,
            result.artists[0].name)

    def __on_end_of_track(self, data):
        if not self.current is None:
            self.emit(self.PLAY_END, self.current)
            self.playing = False
            self.current = None

    def __on_connection_state_updated(self, session):
        if self.session.connection.state is spotify.ConnectionState.LOGGED_IN:
            self.__logged_in.set()
