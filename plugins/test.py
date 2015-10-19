from slackbot.bot import respond_to
from singleton import Slackify

@respond_to('play (.*)')
def giveme(message, something):
    message.reply('Here is %s' % something)
