from slackbot.bot import respond_to
from lib.singleton import Slackify
from lib.queue_manager import QueueManager
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
            message.reply(u'Queue {0}: {1}'.format(index, result))
    else:
        result = slackify.player.search(text)
        if len(result):
            index = slackify.queue.queue(result[0], username)
            message.reply(u'Queue {0}: {1}'.format(index, result[0]))
        else:
            message.reply(u'No results for: {0}'.format(text))

@respond_to('^(q|queue)$')
@respond_to('^$')
def queue_list(message,cmd=None,*args):
    result = slackify.queue.next(10)
    if len(result) > 1:
        message.reply(u'Upcoming:\n{0}'.format(u'\n'.join(map(unicode, result))))
    elif len(result) == 1:
        message.reply(u'Last song in queue:\n{0}'.format(result[0]))
    else:
        message.reply('The queue is empty')

@respond_to('^(n|next|start)$')
def queue_next(message, cmd, *args):
    nxt = slackify.queue.next()
    # Get the current user
    username = slackify.client.users[message.body["user"]]['name']
    # Current queue
    current_queue = slackify.queue.get_queue()

    # Like the error says
    if slackify.player.playing == True and \
        slackify.player.mode == QueueManager.MODE_QUEUE and \
        current_queue != None and \
        current_queue.user != username:
            message.reply('Can only skip songs you queued')
    # There is something in the queue AND
    #   Nothing playing OR
    #   Nothing in the queue and nothing is playing OR
    #   User listening a song (s)he queued OR
    #   Just playing a single song OR
    #   Random/Related playing mode

    elif nxt != None and \
        (   slackify.player.current == None or \
            (current_queue == None and slackify.player.playing == False) or \
            current_queue.user == username or \
            slackify.player.mode == slackify.player.MODE or \
            slackify.player.mode in [QueueManager.MODE_RELATED, QueueManager.MODE_RANDOM]):
                slackify.queue.current(nxt.id)
                return slackify.player.play(nxt.song, slackify.queue.MODE_QUEUE)
    # Start a related/random song
    if slackify.queue.mode == QueueManager.MODE_RELATED:
        nxt = slackify.player.related(single=True)
        if nxt:
            return slackify.player.play(nxt, QueueManager.MODE_RELATED)

    # Try a random song
    nxt = slackify.queue.random()
    if nxt:
        return slackify.player.play(nxt.song, QueueManager.MODE_RANDOM)

    message.reply('There are no songs to play')


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
            message.reply(u'Removed {0}'.format(deleted))
        else:
            message.reply(u'Could not remove: {0}'.format(deleted))

@respond_to('^mode$')
@respond_to('^mode (related|random)')
def queue_mode(message, mode=None):
    if mode:
        slackify.queue.mode = mode
    message.reply(u'Playing {0} songs when the queue is empty'.format(slackify.queue.mode))
