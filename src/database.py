import sqlite3


class Database:

    def __init__(self):
        self.conn = sqlite3.connect("database/game.db")
        self.create_table()
        self.create_save_table()
        self.create_saved_enemies_table()

    # RANKING

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
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT player_name, score, level
            FROM scores
            ORDER BY score DESC
            LIMIT 10
        """)

        return cursor.fetchall()

    # PARTIDA GUARDADA

    def create_save_table(self):

        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS saved_game (
                id INTEGER PRIMARY KEY,
                player_name TEXT NOT NULL,
                player_x INTEGER NOT NULL,
                player_y INTEGER NOT NULL,
                health INTEGER NOT NULL,
                score INTEGER NOT NULL,
                experiencia INTEGER NOT NULL,
                level INTEGER NOT NULL,
                experiencia_siguiente INTEGER NOT NULL,
                weapon_damage INTEGER NOT NULL,
                ammo INTEGER NOT NULL
            )
        ''')

        self.conn.commit()

    def save_game(
        self,
        player_name,
        player_x,
        player_y,
        health,
        score,
        experiencia,
        level,
        experiencia_siguiente,
        weapon_damage,
        ammo,
        enemies
    ):

        cursor = self.conn.cursor()

        # Guardar información principal
        cursor.execute('''
            INSERT OR REPLACE INTO saved_game (
                id,
                player_name,
                player_x,
                player_y,
                health,
                score,
                experiencia,
                level,
                experiencia_siguiente,
                weapon_damage,
                ammo
            )
            VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            player_name,
            player_x,
            player_y,
            health,
            score,
            experiencia,
            level,
            experiencia_siguiente,
            weapon_damage,
            ammo
        ))

        # Borrar enemigos guardados anteriormente
        cursor.execute('DELETE FROM saved_enemies')

        # Guardar enemigos actuales
        for enemy in enemies:

            cursor.execute('''
                INSERT INTO saved_enemies (
                    enemy_type,
                    x,
                    y,
                    health
                )
                VALUES (?, ?, ?, ?)
            ''', (
                enemy.type,
                enemy.rect.x,
                enemy.rect.y,
                enemy.health
            ))

        self.conn.commit()

    def load_game(self):

        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT
                player_name,
                player_x,
                player_y,
                health,
                score,
                experiencia,
                level,
                experiencia_siguiente,
                weapon_damage,
                ammo
            FROM saved_game
            WHERE id = 1
        ''')

        return cursor.fetchone()

    def load_enemies(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT
                enemy_type,
                x,
                y,
                health
            FROM saved_enemies
        ''')
        return cursor.fetchall()

    def create_saved_enemies_table(self):
        
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS saved_enemies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enemy_type TEXT NOT NULL,
                x INTEGER NOT NULL,
                y INTEGER NOT NULL,
                health INTEGER NOT NULL
            )
        ''')

        self.conn.commit()

    def has_saved_game(self):

        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT id
            FROM saved_game
            WHERE id = 1
        ''')

        return cursor.fetchone() is not None

    def delete_saved_game(self):

        cursor = self.conn.cursor()

        cursor.execute('''
            DELETE FROM saved_game
            WHERE id = 1
        ''')

        self.conn.commit()

    def close(self):
        self.conn.close()
        