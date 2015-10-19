import time
import sqlite3
from spotifyplayer import Song

class Queue:
    def from_db(self, record):
        self.id = record["id"]
        self.song = Song(record["uri"], record["title"], record["artist"])
        self.user = record["user"]
        self.added = record["added"]
        return self

class QueueManager:
    def __init__(self, player, db):
        self.player = player
        self.db = db
        self.current_id = 0
        self.__db_init()

    def queue(self, song, user):
        c = self.db.cursor()
        c.execute("""
            INSERT INTO queue(uri, title, artist, user, added,deleted)
            VALUES(?,?,?,?,?,?)
            """,
            (
                song.uri,
                song.title,
                song.artist,
                user,
                int(time.time()),
                0
            ))
        return c.lastrowid

    def clear(self):
        c = self.db.cursor()
        c.execute("DELETE FROM queue")
        self.current_id = 0

    def current(self, index):
        self.current_id = index

    def random(self, limit=1):
        c = self.db.cursor()
        c.execute("""
            SELECT *
            FROM queue
            WHERE
                id > ?
            AND
                deleted = 0
            ORDER BY RANDOM()
            LIMIT ?
            """,
            (self.current_id,limit))
        return self.__convert_result(c, limit)

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
                deleted INTEGER
            )""")
        self.db.commit()
