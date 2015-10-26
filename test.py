import unittest
from tests.player import PlayerTest
from tests.queue import QueueTest
from tests.plugin_player import PluginPlayerTest

import slackify
from lib.singleton import Slackify

if __name__ == '__main__':
    slackify.main(':memory:')
    sy = Slackify()
    sy.bot.channelid = 'test'
    unittest.main()
