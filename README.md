# slackify
Slack bot to play/queue Spotify

## Installation

TODO: some python libs, spotify keys and slackbot configs

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
