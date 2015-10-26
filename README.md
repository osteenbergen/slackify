# slackify
Slack bot to play/queue Spotify

## Installation

### Ubuntu

#### Slack
Install PIP package for python
```
sudo apt-get install python-pip
sudo pip install -r requirements
```
##### Generate the slack api token

First you need to get the slack api token for your bot. You have two options:

1. If you use a [bot user integration](https://api.slack.com/bot-users) of slack, you can get the api token on the integration page.
2. If you use a real slack user, you can generate an api token on [slack web api page](https://api.slack.com/web).

##### Configure the api token

Then you need to configure the `API_TOKEN` in a python module `slackbot_settings.py`, which must be located in a python import path.

slackbot_settings.py:

```python
API_TOKEN = "<your-api-token>"
```

Alternatively, you can use the environment variable `SLACKBOT_API_TOKEN`.

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

### Search
```
@slackify: search <query>
```
To play a song from a search result use:
```
@slackify: play <search_number>
```
Search results are stored per user, you can only play from your own search result

## TODO:
- Player controls (started)
  - ```@slackify: stop```: Stop current song (and do not play queue)
  - ```@slackify: next```: Skip current song if you queued it
  - ```@slackify: volume <up/down> <number>```: Change the volume
- Queueing (started)
  - ```@slackify: queue <query>```: Add a number to the queue
  - ```@slackify: remove <queue_number>```: Remove a song you queued
- Voting (planned) 
  - ```@slackify: vote <queue_number>```: Remove a song someone queued
  - ```@slackify: vote next```: Vote to skip current song
- Play from history if queue is empty (planning)
- Admin (future)
  - Configuration file should list one or more admins
  - ```@slackify: admin add <user>```: Add user as admin
  - ```@slackify: admin remove <user>```: Remove user as admin
