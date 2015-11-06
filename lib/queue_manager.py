import time
import sqlite3
from spotifyplayer import Song, SpotifyPlayer

class Queue:
    def from_db(self, record):
        self.id = record["id"]
        self.song = Song(record["uri"], record["title"], record["artist"], record["duration"])
        self.user = record["user"]
        self.added = record["added"]
        return self
    def __str__(self):
        return "%s - %s (%s)" % (self.id, self.song, self.user)

class QueueManager:
    MODE_QUEUE = "queue"
    MODE_RANDOM = "random"
    def __init__(self, player, db, settings):
        self._settings = settings
        self.player = player

        self.db = db
        self.__db_init()

        self.player.on(SpotifyPlayer.PLAY_END, self.on_track_end)
        self.current_id = self.current_index()
        self.current_queue = None

    def queue(self, song, user):
        c = self.db.cursor()
        c.execute("""
            INSERT INTO queue(uri, title, artist, user, added, duration,deleted)
            VALUES(?,?,?,?,?,?,?)
            """,
            (
                song.uri,
                song.title,
                song.artist,
                user,
                int(time.time()),
                song.duration,
                0
            ))
        c.close()
        self.db.commit()
        return c.lastrowid

    def clear(self):
        c = self.db.cursor()
        c.execute("DELETE FROM queue")
        self.current_id = 0

    def current(self, index):
        c = self.db.cursor()
        c.execute("""
            INSERT OR REPLACE INTO queue_data(key, num)
            VALUES(?,?)
        """, ("current",index))
        c.close()
        self.db.commit()
        self.current_id = index

    def get_queue(self, index=None):
        if index == None:
            index = self.current_id
        c = self.db.cursor()
        c.execute("""
            SELECT *
            FROM queue
            WHERE
                id = ?
            LIMIT 1
            """,
            (index,))
        return self.__convert_result(c, 1)

    def current_index(self):
        c = self.db.cursor()
        c.execute("""
            SELECT *
            FROM queue_data
            WHERE
                key = 'current'
            LIMIT 1
            """)
        data = c.fetchone()
        if data == None:
            return 0
        else:
            return data['num']

    def random(self, limit=1):
        c = self.db.cursor()

        c.execute("""
            SELECT *
            FROM queue
            WHERE
                deleted = 0
            ORDER BY RANDOM()
            LIMIT ?
            """,
            (limit,))
        return self.__convert_result(c, limit)

    def by_user(self, user, limit=1):
        c = self.db.cursor()
        c.execute("""
            SELECT *
            FROM queue
            WHERE
                user = ?
            AND
                deleted = 0
            ORDER BY id DESC
            LIMIT ?
            """,
            (user,limit))
        return self.__convert_result(c, limit)

    def delete(self, index):
        c = self.db.cursor()
        try:
            c.execute("""
                UPDATE queue
                SET deleted=1
                WHERE
                    id = ?
            """, (index,))
            c.close()
            self.db.commit()
            return True
        except:
            return False

    def next(self, limit=1):
        c = self.db.cursor()
        c.execute("""
            SELECT *
            FROM queue
            WHERE
                id > ?
            AND
                deleted = 0
            LIMIT ?
            """,
            (self.current_id,limit))
        return self.__convert_result(c, limit)

    def on_track_end(self, current):
        nxt = self.next()
        q = self.get_queue()
        if nxt:
            self.current(nxt.id)
            self.player.play(nxt.song, self.MODE_QUEUE)
        else:
            random = self.random()
            if random != None:
                self.player.play(random.song, self.MODE_RANDOM)

        if self.player.mode == self.MODE_QUEUE and \
            q != None and \
            q.song == current and \
            self.player.playing:
                self.current(self.current_id + 1)

    def __convert_result(self, cursor, limit):
        if limit == 1:
            data = cursor.fetchone()
            if data == None:
                return None
            return Queue().from_db(data)
        else:
            return map(lambda x: Queue().from_db(x), cursor.fetchall())

    def __db_init(self):
        c = self.db.cursor()
        # Create table
        c.execute("""
            CREATE TABLE IF NOT EXISTS queue(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uri TEXT,
                title TEXT,
                artist TEXT,
                user TEXT,
                added INTEGER,
                duration INTEGER,
                deleted INTEGER
            )""")
        self.db.commit()
        c.execute("""
            CREATE TABLE IF NOT EXISTS queue_data(
                key TEXT PRIMARY KEY,
                value TEXT,
                num INTEGER
            )""")
        self.db.commit()
