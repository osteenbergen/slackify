import unittest
import time
from lib.singleton import Slackify
from lib.spotifyplayer import Song

class QueueTest(unittest.TestCase):
    def setUp(self):
        self.slackify = Slackify()
        self.queue = self.slackify.queue
        self.queue.clear()
        self.song = Song(
            "spotify:track:31v2AQlx4pDI7kmnLxBkem",
            "Mmm Mmm Mmm Mmm",
            "Crash Test Dummies")
        self.short_song = Song(
            "spotify:track:29d7RcMCDcMLM7AHT7QbDB",
            "Cheney",
            "Brakes")
    def tearDown(self):
        self.queue.clear()

    def test_queue(self):
        time_now = int(time.time())
        qid = self.queue.queue(self.song, "test")
        self.assertIsInstance(qid, int, "Should be a number")
        nxt = self.queue.next()
        self.assertIsNotNone(nxt, "Should have a valid next song")
        self.assertEqual(nxt.song.uri, self.song.uri, "URI should match")
        self.assertEqual(nxt.song.title, self.song.title, "Titles should match")
        self.assertEqual(nxt.song.artist, self.song.artist, "Artist should match")
        self.assertEqual(nxt.user, "test", "User should match")
        self.assertGreaterEqual(nxt.added, time_now, "Time should be set correctly")

        qid_next = self.queue.queue(self.song, "test")
        self.assertGreater(qid_next, qid, "Should be the second song queued")

    def test_no_next(self):
        nxt = self.queue.next()
        self.assertIsNone(nxt, "Queue should be empty")

    def test_next_multiple(self):
        self.queue.queue(self.song, "test")
        self.queue.queue(self.short_song, "test2")
        nxt_list = self.queue.next(10)
        self.assertEqual(len(nxt_list), 2, "Should have two numbers queued")
        self.assertEqual(nxt_list[0].song.uri, self.song.uri, "URI should match")
        self.assertEqual(nxt_list[0].user, "test", "User should match")
        self.assertEqual(nxt_list[1].song.uri, self.short_song.uri, "URI should match")
        self.assertEqual(nxt_list[1].user, "test2", "User should match")

    def test_random(self):
        qid = self.queue.queue(self.song, "test")
        qid2 = self.queue.queue(self.short_song, "test2")
        random = self.queue.random()
        self.assertIsNotNone(random, "SHould have a random resylt")
        self.assertIn(random.id, [qid, qid2],"Should be one of the songs added")

    def test_current_id(self):
        self.queue.queue(self.song, "test")
        self.queue.queue(self.short_song, "test2")
        self.queue.current(1)
        nxt = self.queue.next()
        self.assertEqual(nxt.id, 2, "Should be the second song queued")

    def test_clear(self):
        self.queue.queue(self.song, "test")
        self.queue.clear()
        nxt = self.queue.next()
        self.assertIsNone(nxt, "Queue should be empty")
