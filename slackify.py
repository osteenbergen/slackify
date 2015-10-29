#!/usr/bin/env python
import logging
import sqlite3
from lib.bot import SlackifyBot
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from lib.singleton import Slackify
from lib.spotifyplayer import SpotifyPlayer
from lib.queue_manager import QueueManager

def db_init(db):
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    db.row_factory = dict_factory

def main(db_location):
    slackify = Slackify()
    slackify.log = logging.basicConfig(level=logging.INFO)
    slackify.bot = SlackifyBot('slackifytesting')
    slackify.db = sqlite3.connect(db_location, check_same_thread=False)
    slackify.client = slackify.bot.client
    db_init(slackify.db)
    slackify.player = SpotifyPlayer()
    slackify.player.on(SpotifyPlayer.PLAY_TRACK, slackify.bot.on_play)
    slackify.player.on(SpotifyPlayer.PLAY_PAUSE, slackify.bot.on_pause)
    slackify.player.on(SpotifyPlayer.PLAY_PLAY, slackify.bot.on_play)
    slackify.player.on(SpotifyPlayer.PLAY_STOP, slackify.bot.on_stop)
    slackify.queue = QueueManager(slackify.player, slackify.db)
    return slackify

if __name__ == "__main__":
    slackify = main('slackify.db')
    #slackify.client.send_message(slackify.channel, "Music Maestro!")
    slackify.bot.run()
