from slackbot.bot import Bot

class SlackifyBot(Bot):
    def __init__(self, channelname):
        super(SlackifyBot,self).__init__()
        self.username = self._client.username
        self.userid = self._client.find_user_by_name(self.username)
        self.channelname = channelname

        # Get the defaulf music channel ID
        self.channelid = None
        for c in self._client.channels:
            channel = self._client.channels[c]
            if "name" in channel and channel["name"] == "music":
                self.channelid = channel["id"]
                break
        if self.channelid == None:
            raise "Could not find '%s' channel" % self.channelname

    def verify(self,message):
        if self.channelid != message.body["channel"]:
            return False
        return True

    def client(self):
        return self._client
