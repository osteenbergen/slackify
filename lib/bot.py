from slackbot.bot import Bot

class SlackifyBot(Bot):
    def __init__(self, channelname=None):
        super(SlackifyBot,self).__init__()
        self.username = self._client.username
        self.userid = self._client.find_user_by_name(self.username)
        self.channelname = channelname

        # Get the defaulf music channel ID
        self.channelid = None
        if self.channelname != None:
            for c in self._client.channels:
                channel = self._client.channels[c]
                if "name" in channel and channel["name"] == self.channelname:
                    self.channelid = channel["id"]
                    break
            if self.channelid == None:
                raise "Could not find '%s' channel" % self.channelname

    def verify(self,message):
        if self.channelid != None:
            if self.channelid != message.body["channel"]:
                message.reply("Incorrect channel, use %s" % self.channelname)
                return False
        return True

    @property
    def client(self):
        return self._client

    def on_start(self, song):
        self._client.rtm_send_message(self.channelid, "Playing: %s" % song)

    def on_pause(self, song):
        self._client.rtm_send_message(self.channelid, "Pausing: %s" % song)

    def on_play(self, song):
        self._client.rtm_send_message(self.channelid, "Playing: %s" % song)

    def on_stop(self, song):
        self._client.rtm_send_message(self.channelid, "Stopping: %s" % song)
