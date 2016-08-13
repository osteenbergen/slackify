from slackbot.bot import respond_to, listen_to
from lib.singleton import Slackify

slackify = Slackify()

@respond_to('^reconnect$')
def reconnect(message,*args):
    slackify.client.reconnect()
    message.reply("Reconnected to Slack")

@listen_to('has joined')
def listen(message, *args):
    print "Reconnecting as new user joined"
    slackify.client.reconnect()

@respond_to('help')
def help(message, *args):
    message.reply("""Available commands:
- `play QUERY`: play a song now
- `next`: Skip current song
- `queue QUERY`: queue a song
- `queue`: Show the current queue
- `search QUERY`: search spotify
- `play NUMBER`: play song from search result
- `queue NUMBER`: queue song from search result
- `remove NUMBER`: Remove number from queue/playlist
""")
