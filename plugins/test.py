from slackbot.bot import respond_to
from lib.singleton import Slackify
import json

print "Test loaded"
@respond_to('(.*)')
def giveme(message,text,*args):
    message.reply('Got text : "%s" : %s' % (text,message.body))
