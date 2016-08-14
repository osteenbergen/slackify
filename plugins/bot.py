from slackbot.bot import respond_to, listen_to
from lib.singleton import Slackify

slackify = Slackify()

@respond_to('^(show|hide) album art$')
def album_art(message,show, *args):
    slackify.bot.show_album_art = show == "show"
    if slackify.bot.show_album_art:
        message.reply("Showing album art")
    else:
        message.reply("Hiding album art")

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
- `start`: start playing
- `stop`: stop playing
- `pause`: pause playing
- `play`: continue playing
- `play QUERY`: play a song now
- `next`: Skip current song
- `queue QUERY`: queue a song
- `queue`: Show the current queue
- `search QUERY`: search spotify
- `play NUMBER`: play song from search result
- `queue NUMBER`: queue song from search result
- `remove NUMBER`: Remove number from queue/playlist
- `related`: Show related songs to current song
- `mode related`: Play related songs when queue is empty
- `mode random`: Play previously played songs when queue is empty
- `show album art`: Display album art when starting a song
- `hide album art`: Do not show album art
""")
