import os
import sqlite3 as sql

class Database:

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        db_path = os.path.join(
            base_dir,
            "../grpa_backup/app/modules", "..", "database", "app.db"
        )

        self.conn = sql.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_tables(self):

        with open("../database/migrations/tables.sql", "r", encoding="utf-8") as f:
            script = f.read()

        self.cursor.executescript(script)
        self.conn.commit()

        self.close()

        return self

    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    db = Database()
    print(db.create_tables())