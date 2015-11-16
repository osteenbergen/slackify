from slackbot.bot import Bot
from lib.spotifyplayer import SpotifyPlayer
from lib.queue_manager import QueueManager

class SlackifyBot(Bot):
    def __init__(self, player, queue, settings=None):
        super(SlackifyBot,self).__init__()
        self._settings = settings
        self._player = player
        self._queue = queue
        self.username = self._client.username
        self.userid = self._client.find_user_by_name(self.username)
        self.channelname = self._settings.FIXED_CHANNEL

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

        # Hooks to the eventemitter
        self._player.on(SpotifyPlayer.PLAY_TRACK, self._on_start)
        self._player.on(SpotifyPlayer.PLAY_PAUSE, self._on_pause)
        self._player.on(SpotifyPlayer.PLAY_PLAY, self._on_play)
        self._player.on(SpotifyPlayer.PLAY_STOP, self._on_stop)

    def verify(self,message):
        if self.channelid != None:
            if self.channelid != message.body["channel"]:
                message.reply("Incorrect channel, use %s" % self.channelname)
                return False
        return True

    @property
    def client(self):
        return self._client

    def _on_start(self, song):
        if self._player.mode == QueueManager.MODE_QUEUE:
            queue = self._queue.get_queue()
            self._client.rtm_send_message(
                self.channelid,
                "Playing queue %s: %s (%s)" % (
                    queue.id,
                    queue.song,
                    queue.user
                ))
        elif self._player.mode == QueueManager.MODE_RANDOM:
            history = self._queue.find(song)
            if len(history) == 1:
                self._client.rtm_send_message(
                    self.channelid,
                    "Playing random song: %s" % history[0])
            else:
                self._client.rtm_send_message(
                    self.channelid,
                    "Playing random song which was queued %d times: %s" % (len(history),history[0]))
        else:
            self._client.rtm_send_message(self.channelid, "Playing: %s" % song)

    def _on_pause(self, song):
        self._client.rtm_send_message(self.channelid, "Pausing: %s" % song)

    def _on_play(self, song):
        self._client.rtm_send_message(self.channelid, "Playing: %s" % song)

    def _on_stop(self, song):
        self._client.rtm_send_message(self.channelid, "Stopping: %s" % song)
