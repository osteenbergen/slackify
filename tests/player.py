import unittest
import time
from lib.singleton import Slackify
from lib.spotifyplayer import Song

class PlayerTest(unittest.TestCase):
    def setUp(self):
        self.slackify = Slackify()
        self.player = self.slackify.player
        self.song = Song(
            "spotify:track:31v2AQlx4pDI7kmnLxBkem",
            "Mmm Mmm Mmm Mmm",
            "Crash Test Dummies")
        self.short_song = Song(
            "spotify:track:29d7RcMCDcMLM7AHT7QbDB",
            "Cheney",
            "Brakes")

    def test_play(self):
        song_info = self.player.play(self.song)
        self.assertEqual(self.song, song_info, "Should return same song")
        self.assertEqual(self.player.current, self.song, "Should return same song")
        self.assertEqual(self.player.playing, True, "Song should be playing")
        print("\nYou should hear a song playing: %s - %s" %
            (self.song.artist, self.song.title))
        time.sleep(3)

    def test_pause(self):
        song_info = self.player.play(self.song)
        self.assertTrue(self.player.playing, "Song should be playing")
        print("\nYou should hear a song playing, pause and continue: %s - %s" %
            (self.song.artist, self.song.title))
        time.sleep(2)

        print("Song should now pause")
        self.player.playpause()
        self.assertFalse(self.player.playing, "Song should be paused")
        time.sleep(1)

        print("Song should now continue")
        self.player.playpause()
        self.assertTrue(self.player.playing, "Song should be playing")
        time.sleep(2)

    def test_stop(self):
        song_info = self.player.play(self.song)
        self.assertTrue(self.player.playing, "Song should be playing")
        print("\nYou should hear a song playing and stop: %s - %s" %
            (self.song.artist, self.song.title))
        time.sleep(4)

        print("Song should now stop")
        self.player.stop()
        self.assertFalse(self.player.playing, "Song should be stopped")
        self.assertEqual(self.player.current, None, "Current should not exist")

    def test_emit(self):
        self.emit_start_trigger = False
        self.emit_play_trigger = False
        self.emit_pause_trigger = False
        self.emit_stop_trigger = False
        self.emit_playing = self.song

        def start_trigger(song):
            self.assertEqual(song, self.emit_playing, "Correct song should start")
            self.emit_start_trigger = True

        def play_trigger(song):
            self.assertEqual(song, self.emit_playing, "Correct song should play")
            self.emit_play_trigger = True

        def pause_trigger(song):
            self.assertEqual(song, self.emit_playing, "Correct song should pause")
            self.emit_pause_trigger = True

        def stop_trigger(song):
            self.assertEqual(song, self.emit_playing, "Correct song should stop")
            self.emit_stop_trigger = True

        self.player.on(self.player.PLAY_TRACK, start_trigger)
        self.player.on(self.player.PLAY_PLAY, play_trigger)
        self.player.on(self.player.PLAY_PAUSE, pause_trigger)
        self.player.on(self.player.PLAY_STOP, stop_trigger)

        self.player.play(self.emit_playing)
        time.sleep(5)
        self.player.playpause()
        time.sleep(1)
        self.player.playpause()
        time.sleep(3)
        self.player.stop()
        time.sleep(2)
        self.assertTrue(self.emit_start_trigger, "Start trigger should have fired")
        self.assertTrue(self.emit_play_trigger, "Play trigger should have fired")
        self.assertTrue(self.emit_pause_trigger, "Pause trigger should have fired")
        self.assertTrue(self.emit_stop_trigger, "Stop trigger should have fired")

        self.player.off(self.player.PLAY_TRACK, start_trigger)
        self.player.off(self.player.PLAY_PLAY, play_trigger)
        self.player.off(self.player.PLAY_PAUSE, pause_trigger)
        self.player.off(self.player.PLAY_STOP, stop_trigger)

    def test_emit_end(self):
        self.emit_playing = self.short_song
        self.emit_end_trigger = False
        def end_trigger(song):
            self.assertEqual(song, self.emit_playing, "Correct song should end")
            self.emit_end_trigger = True

        self.player.on(self.player.PLAY_END, end_trigger)
        self.player.play(self.emit_playing)
        time.sleep(15)
        self.assertTrue(self.emit_end_trigger, "End trigger should have fired")
        self.player.off(self.player.PLAY_END, end_trigger)

    def test_search(self):
        result = self.player.search(str(self.song))
        found = False
        for r in result:
            found |= r == self.song
        self.assertTrue(found, "Should find the song")
