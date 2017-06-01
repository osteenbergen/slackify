from slackbot.bot import respond_to
from lib.singleton import Slackify


slackify = Slackify()

@respond_to('^(p|play) (.*)$')
def play_song(message,cmd,text,*args):
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
            message.reply(u'No results for: {0}'.format(text))

@respond_to('^(p|play(ing)?)$')
def playing(message,cmd,*args):
    if not slackify.bot.verify(message):
        return
    if cmd == "playing":
        message.reply(u'[{0}] Currently playing: {1}'.format(slackify.player.mode,slackify.player.current))
    elif slackify.player.current != None:
        slackify.player.playpause()
    else:
        message.reply('No song currently playing')

@respond_to('^pause$')
def pause(message,*args):
    if not slackify.bot.verify(message):
        return
    if slackify.player.current != None:
        slackify.player.playpause()
    else:
        message.reply('No song currently playing')

@respond_to('^(s|search) (.*)$')
def search_song(message,cmd,text,*args):
    # Do not verify the message to allow for direct messages
    result = slackify.player.search(text, message.body["user"])
    if len(result):
        songs = []
        for idx, song in enumerate(result):
            songs.append(u'{0} | {1}'.format(idx + 1, song))
        message.reply(u'Search result:\n{0}'.format("\n".join(songs)))
    else:
        message.reply(u'No results for: {0}'.format(text))

@respond_to('^(rel|related)$')
def related_song(message,cmd,*args):
    # Do not verify the message to allow for direct messages
    result = slackify.player.related(user=message.body["user"])
    if result and len(result):
        songs = []
        for idx, song in enumerate(result):
            songs.append(u'{0} | {1}'.format(idx + 1, song))
        message.reply(u'Related songs for {0}:\n{1}'.format(
            slackify.player.current,
            "\n".join(songs)))
    else:
        message.reply(u'No related results')

@respond_to('^history$')
def history(message):
    if len(slackify.player.history) > 0:
        songs = []
        for idx, song in enumerate(slackify.player.history):
            songs.append(u'{0} | {1}'.format(idx + 1, song))
        message.reply(u'Recently played songs:\n{0}'.format(
            "\n".join(songs)))
    else:
        message.reply(u'Didn\'t play any song yet')

@respond_to('^stop$')
def stop(message,*args):
    if not slackify.bot.verify(message):
        return
    slackify.player.stop()
