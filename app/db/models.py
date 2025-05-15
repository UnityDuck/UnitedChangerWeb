import sqlite3
import os


def get_db():
    """Получение подключения к базе данных с правильным путем."""
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../database/database.db')
    if not os.path.exists(db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Инициализация базы данных (создание таблиц)."""
    with get_db() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                avatar TEXT DEFAULT "",
                api_key TEXT UNIQUE
            )
        ''')
        conn.commit()
