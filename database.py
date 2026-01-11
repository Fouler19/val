import sqlite3

class DatabaseManager:
    def __init__(self, database):
        self.database = database

    def get_winners_count(self, prize_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute('SELECT COUNT(*) FROM winners WHERE prize_id = ?', (prize_id,))
            return cur.fetchone()[0]

    def add_winner(self, user_id, prize_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute('SELECT 1 FROM winners WHERE user_id = ? AND prize_id = ?', (user_id, prize_id))
            if cur.fetchone():
                return False
            cur.execute('INSERT INTO winners (user_id, prize_id) VALUES (?, ?)', (user_id, prize_id))
            return True

    def get_rating(self):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT u.username, COUNT(w.prize_id) as prizes_count
                FROM users u
                LEFT JOIN winners w ON u.user_id = w.user_id
                GROUP BY u.user_id
                ORDER BY prizes_count DESC
                LIMIT 10
            ''')
            return cur.fetchall()
