#!/usr/bin/env python
import logging
import sqlite3
import slackbot_settings
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
    # Create the singleton class to map all objects
    # Makes writing plugins easier
    slackify = Slackify()
    # Store the settings
    slackify.settings = slackbot_settings
    # Create a logger
    slackify.log = logging.basicConfig(level=logging.INFO)

    # Database connection
    slackify.db = sqlite3.connect(db_location, check_same_thread=False)
    # Output dicts instead of arrays when querying
    db_init(slackify.db)

    # Start spotify
    slackify.player = SpotifyPlayer(slackify.settings)

    # The slackbot itself
    slackify.bot = SlackifyBot(slackify.player, slackify.settings)
    # Slack client, so we can send messages
    slackify.client = slackify.bot.client

    # Start the queue
    slackify.queue = QueueManager(slackify.player, slackify.db, slackify.settings)
    return slackify

if __name__ == "__main__":
    slackify = main('slackify.db')
    #slackify.client.send_message(slackify.channel, "Music Maestro!")
    slackify.bot.run()
