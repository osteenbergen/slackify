from slackbot.bot import listen_to
from lib.singleton import Slackify
import json

print "Test loaded"
@listen_to('^\<@(\w+)\>(:|)*$')
def giveme(message,*args):
    slackify = Slackify()
    if not slackify.bot.verify(message):
        return
    message.reply('Hello World! : "%s"' % slackify.bot.userid)
