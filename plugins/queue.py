from slackbot.bot import respond_to
from lib.singleton import Slackify
import json

slackify = Slackify()

@respond_to('^(q|queue) (.*)$')
def queue_song(message,cmd,text,*args):
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
    result = slackify.queue.next(10)
    if len(result) > 1:
        message.reply('Upcoming:\n%s' % "\n".join(map(str, result)))
    elif len(result) == 1:
        message.reply('Last song in queue:\n%s' % result[0])
    else:
        message.reply('The queue is empty')

@respond_to('^(n|next|start)$')
def queue_next(message, cmd, *args):
    nxt = slackify.queue.next()
    if nxt == None:
        nxt = slackify.queue.random()
        if nxt != None:
            slackify.player.play(nxt.song, slackify.queue.MODE_RANDOM)
        else:
            message.reply('There are no songs to play')
        return
    username = slackify.client.users[message.body["user"]]['name']
    current_queue = slackify.queue.get_queue()
    if slackify.player.current == None or current_queue == None or current_queue.user == username:
        slackify.queue.current(nxt.id)
        slackify.player.play(nxt.song, slackify.queue.MODE_QUEUE)
    elif current_queue != None and current_queue.user != username:
        message.reply('Can only skip songs you queued')

@respond_to('^(r|rm|remove) (last|\d+)$')
def queue_remove(message, cmd, position):
    number = position
    username = slackify.client.users[message.body["user"]]['name']
    if position == "last":
        nxt = slackify.queue.by_user(username)
        if nxt == None:
            message.reply("You didn't queue anything yet")
            return
        else:
            number = nxt.id
    deleted = slackify.queue.get_queue(number)
    if deleted == None:
        message.reply('Invalid index')
    else:
        state = slackify.queue.delete(number)
        if state:
            message.reply('Removed %s' % deleted)
        else:
            message.reply('Could not remove: %s' % deleted)
