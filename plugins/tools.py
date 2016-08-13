from slackbot.bot import respond_to, listen_to
from lib.singleton import Slackify

slackify = Slackify()

@respond_to('^reconnect$')
def reconnect(message,*args):
    slackify.client.reconnect()
    message.reply("Reconnected to Slack")

@listen_to('has joined')
def listen(message, *args):
    print "Reconnecting as new user joined"
    slackify.client.reconnect()
