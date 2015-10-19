import unittest
from tests.player import PlayerTest
from tests.queue import QueueTest
from tests.plugin_player import PluginPlayerTest

import slackify
if __name__ == '__main__':
    slackify.main(':memory:')
    unittest.main()
