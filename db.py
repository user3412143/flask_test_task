import sqlite3
from flask import g

class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    @property
    def connection(self):
        if 'db' not in g:
            g.db = sqlite3.connect(self.db_name)
            g.db.row_factory = sqlite3.Row
        return g.db

    def create_tables(self):
        with self.connection as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER \
                    PRIMARY KEY, username TEXT, password TEXT, token TEXT, \
                    email TEXT, user_dir TEXT)')
            conn.execute('CREATE TABLE IF NOT EXISTS tracks (id INTEGER \
                    PRIMARY KEY, username TEXT, track_name TEXT, fake_name TEXT, \
                    description TEXT, location TEXT, link TEXT)')

    def insert_user(self, username: str, password: str, email: str):
        with self.connection as conn:
            conn.execute('INSERT INTO users (username, password, email) \
                    VALUES (?, ?, ?)', (username, password, email))

    def get_user(self, username: str):
        with self.connection as conn:
            cursor = conn.execute('SELECT * FROM users WHERE username = ?', (username,))
            return cursor.fetchone()

    def get_token(self, username: str):
        with self.connection as conn:
            cursor = conn.execute('SELECT token FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def update_user_token(self, username: str, token: str):
        with self.connection as conn:
            conn.execute('UPDATE users SET token = ? WHERE username = ?', (token, username))

    def get_user_dir(self, username: str):
        with self.connection as conn:
            cursor = conn.execute('SELECT user_dir FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def set_user_dir(self, username: str, user_dir: str):
        with self.connection as conn:
            conn.execute('UPDATE users SET user_dir = ? WHERE \
                    username = ?', (user_dir, username))

    def get_tracks(self, username: str):
        with self.connection as conn:
            cursor = conn.execute('SELECT * FROM tracks WHERE username = ?', (username,))
            tracks = cursor.fetchall()
            return tracks

    def add_track(self, username: str, track_name: str, fake_name: str, path: str):
        with self.connection as conn:
            cursor = conn.execute('INSERT INTO tracks (username, track_name, \
                    fake_name, location) VALUES (?, ?, ?,?)', (username, track_name, fake_name, path))
            conn.commit()
