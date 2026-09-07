import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("database/game.db")
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                level INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def save_scores(self, player_name, score, level):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO scores (player_name, score, level)
            VALUES (?, ?, ?)
        ''', (player_name, score, level))
        self.conn.commit()

    def get_Raking(self):
        cursor= self.conn.cursor()
        cursor.execute("""
            SELECT player_name, score, level
            FROM scores
            ORDER BY score DESC
            LIMIT 10
        """)
        return cursor.fetchall()

    def close(self):
        self.conn.close()
        