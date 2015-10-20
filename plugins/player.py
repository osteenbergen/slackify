from slackbot.bot import respond_to
from lib.singleton import Slackify

@respond_to('(p|play) (.*)$')
def play_song(message,cmd,text,*args):
    slackify = Slackify()
    if not slackify.bot.verify(message):
        return
    if text.isdigit():
        result = slackify.player.search_history(
            message.body["user"],
            int(text) - 1)
        if result == None:
            message.reply('Not a valid search index ')
        else:
            slackify.player.play(result)
    else:
        result = slackify.player.search(text)
        if len(result):
            slackify.player.play(result[0])
        else:
            message.reply('No results for: %s' % text)

@respond_to('(p|play(ing)?)$')
def playing(message,cmd,*args):
    slackify = Slackify()
    if not slackify.bot.verify(message):
        return
    if cmd == "playing":
        message.reply('Currently playing: %s' % slackify.player.current)
    elif slackify.player.current != None:
        slackify.player.playpause()
    else:
        message.reply('No song currently playing')

@respond_to('pause$')
def playing(message,*args):
    if not slackify.bot.verify(message):
        return
    slackify = Slackify()
    if slackify.player.current != None:
        slackify.player.playpause()
    else:
        message.reply('No song currently playing')

@respond_to('(s|search) (.*)$')
def play_song(message,cmd,text,*args):
    slackify = Slackify()
    # Do not verify the message to allow for direct messages
    result = slackify.player.search(text, message.body["user"])
    if len(result):
        songs = []
        for idx, song in enumerate(result):
            songs.append("%s | %s" %(idx + 1, song))
        message.reply('Search result:\n%s' % "\n".join(songs))
    else:
        message.reply('No results for: %s' % text)
