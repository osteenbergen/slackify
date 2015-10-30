from slackbot.bot import respond_to
from lib.singleton import Slackify
import json

@respond_to('^(q|queue) (.*)$')
def queue_song(message,cmd,text,*args):
    slackify = Slackify()
    username = slackify.client.users[message.body["user"]]['name']
    if not slackify.bot.verify(message):
        return
    if text.isdigit():
        result = slackify.player.search_history(
            message.body["user"],
            int(text) - 1)
        if result == None:
            message.reply('Not a valid search index ')
        else:
            index = slackify.queue.queue(result, username)
            message.reply('Queue %s: %s' % (index, result))
    else:
        result = slackify.player.search(text)
        if len(result):
            index = slackify.queue.queue(result[0], username)
            message.reply('Queue %s: %s' % (index, result[0]))
        else:
            message.reply('No results for: %s' % text)

@respond_to('^(q|queue)$')
def queue_song(message,cmd,*args):
    slackify = Slackify()
    result = slackify.queue.next(10)
    if len(result):
        message.reply('Upcomming:\n%s' % "\n".join(result))
    else:
        message.reply('The queue is empty')