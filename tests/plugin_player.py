import unittest
from plugins import player

class FakeMessage:
    def __init__(self):
        self.output = []
    def reply(self, message):
        self.output.append(message)
    def first_message(self):
        if len(self.output) > 0:
            return self.output[0]
        return None
    @property
    def body(self):
        return {
            'user':'test',
            'channel':'test'
        }

class PluginPlayerTest(unittest.TestCase):
    def setUp(self):
        pass
    def test_play(self):
        msg = FakeMessage()
        player.play_song(msg, "play","Crash Test Dummies - Mmm Mmm Mmm Mmm")
        print msg.first_message()
        self.assertEqual(
            msg.first_message(),
            None,
            "There should not be any output")

    def test_play_not_playing(self):
        msg = FakeMessage()
        player.playing(msg, "play")
        self.assertEqual(
            msg.first_message(),
            "No song currently playing",
            "No song should be playing")
