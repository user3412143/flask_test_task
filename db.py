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
                    PRIMARY KEY, username TEXT, password TEXT, token TEXT, email TEXT)')
            conn.execute('CREATE TABLE IF NOT EXISTS tracks (id INTEGER \
                    PRIMARY KEY, username TEXT, track_name TEXT, description \
                    TEXT, location TEXT, link TEXT)')

    def insert_user(self, username, password, email):
        with self.connection as conn:
            conn.execute('INSERT INTO users (username, password, email) \
                    VALUES (?, ?, ?)', (username, password, email))

    def get_user(self, username):
        with self.connection as conn:
            cursor = conn.execute('SELECT * FROM users WHERE username = ?', (username,))
            return cursor.fetchone()

    def update_user_token(self, username, token):
        with self.connection as conn:
            conn.execute('UPDATE users SET token = ? WHERE username = ?', (token, username))


    def get_tracks(self, username):
        with self.connection as conn:
            cursor = conn.execute('SELECT * FROM tracks WHERE username = ?', (username,))
            tracks = cursor.fetchall()
            return tracks

    def add_track(self, username, track_name, path):
        with self.connection as conn:
            cursor = conn.execute('INSERT INTO tracks (username, track_name, \
                    location) VALUES (?, ?,?)', (username, track_name, path))
            conn.commit()
