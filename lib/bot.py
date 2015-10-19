from slackbot.bot import Bot

class SlackifyBot(Bot):
    def __init__(self):
        super(SlackifyBot,self).__init__()

    def client(self):
        return self._client
