#!/usr/bin/env python

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
    slackify.bot = SlackifyBot()
    slackify.db = sqlite3.connect(db_location)
    slackify.client = slackify.bot.client()

    # Get the defaulf music channel ID
    slackify.channel = None
    for c in slackify.client.channels:
        channel = slackify.client.channels[c]
        if "name" in channel and channel["name"] == "music":
            slackify.channel = channel["id"]
            break
    if slackify.channel == None:
        raise "Could not find music channel"

    db_init(slackify.db)
    slackify.player = SpotifyPlayer()
    slackify.queue = QueueManager(slackify.player, slackify.db)
    return slackify

if __name__ == "__main__":
    slackify = main('slackify.db')
    #slackify.client.send_message(slackify.channel, "Music Maestro!")
    slackify.bot.run()
