from slackbot.bot import respond_to
from lib.singleton import Slackify

@respond_to('(p|play) (.*)$')
def play_song(message,cmd,text,*args):
    slackify = Slackify()
    result = slackify.player.search(text)
    if len(result):
        slackify.player.play(result[0])
    else:
        message.reply('No results for: %s' % text)

@respond_to('(p|play(ing)?)$')
def playing(message,cmd,*args):
    slackify = Slackify()
    if cmd == "playing":
        message.reply('Currently playing: %s' % slackify.player.current)
    elif slackify.player.current != None:
        slackify.player.playpause()
    else:
        message.reply('No song currently playing')

@respond_to('pause$')
def playing(message,*args):
    slackify = Slackify()
    if slackify.player.current != None:
        slackify.player.playpause()
    else:
        message.reply('No song currently playing')
