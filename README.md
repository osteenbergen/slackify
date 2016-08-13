# slackify
Slack bot to play/queue Spotify

Used&Tested daily in our office with a simple setup. Install on a box connected to speakers and enjoy.

## Features
- Searching spotify
- Playing songs
- Queueing songs
- Random song from queue history if queue is empty

## Settings
Create a file called ```slackbot_settings.py``` with the following contents
```python
# Slackbot settings
API_TOKEN = '<token>'
# Force bot to only work on a single channel
FIXED_CHANNEL = 'music'
# Spotify settings
SPOTIFY_USERNAME = '<username>'
SPOTIFY_PASSWORD = '<password>'
SPOTIFY_MARKET = 'NL'

# Folder with the slack commands
PLUGINS = ['plugins']
```

## Installation

### Ubuntu

#### Slack
Install PIP package for python (lins05/slackbot)
```
sudo apt-get install python-pip
sudo pip install -r requirements
```
##### Generate the slack api token

First you need to get the slack api token for your bot. You have two options:

1. If you use a [bot user integration](https://api.slack.com/bot-users) of slack, you can get the api token on the integration page.
2. If you use a real slack user, you can generate an api token on [slack web api page](https://api.slack.com/web).

##### Configure the api token

Then you need to configure the `API_TOKEN` in the python module `slackbot_settings.py`.

#### Spotify
Follow pyspotify installation on https://pyspotify.mopidy.com/en/latest/installation/

or in short:
```
wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/jessie.list
sudo apt-get update
sudo apt-get install python-spotify
```

Get a binary spotify application key and store it in the main folder: https://devaccount.spotify.com/my-account/keys/

Finally install the correct audio driver:
```
sudo apt-get install python-alsaaudio
```

### OSX

Follow instructions for Ubuntu and read the source websites for the spotify python library.

The audio driver for OSX is PyAudio:
```
pip install pyaudio
```

OSX should be detected and use this library, although this is untested

## Commands

### Play
To play a song
```
@slackify: play <query>
```
To pause or continue
```
@slackify: pause
@slackify: play
```
To stop playing
```
@slackify: stop
```

### Search
```
@slackify: search <query>
```
To play a song from a search result use:
```
@slackify: play <search_number>
```
Search results are stored per user, you can only play from your own search result

### Queueing
```
@slackify: queue <query>
```
Or using the search result
```
@slackify: queue <search_numer>
```
Skip your song in the queue
```
@slackify: next
```

## TODO:
- Player controls (started)
  - ```@slackify: volume <up/down> <number>```: Change the volume
- Queueing (started)
  - ```@slackify: remove <queue_number>```: Remove a song you queued
- Voting (planned)
  - ```@slackify: vote <queue_number>```: Remove a song someone queued
  - ```@slackify: vote next```: Vote to skip current song
- Admin (future)
  - Configuration file should list one or more admins
  - ```@slackify: admin add <user>```: Add user as admin
  - ```@slackify: admin remove <user>```: Remove user as admin
