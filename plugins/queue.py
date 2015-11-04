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
    if len(result) > 1:
        message.reply('Upcoming:\n%s' % "\n".join(map(str, result)))
    elif len(result) == 1:
        message.reply('Last song in queue:\n%s' % result[0])
    else:
        message.reply('The queue is empty')

@respond_to('^(next|start)$')
def queue_next(message, cmd, *args):
    slackify = Slackify()
    nxt = slackify.queue.next()
    username = slackify.client.users[message.body["user"]]['name']
    current_queue = slackify.queue.get_queue()
    print current_queue
    if slackify.player.current == None or current_queue == None or current_queue.user == username:
        slackify.player.play(nxt.song)
        slackify.queue.current(nxt.id)
    elif current_queue != None and current_queue.user != username:
        message.reply('Can only skip songs you queued')
