import sqlite3
import os


class User:
    def __init__(self, id=None, username=None, password=None, avatar="", api_key=None):
        self.id = id
        self.username = username
        self.password = password
        self.avatar = avatar
        self.api_key = api_key

    @classmethod
    def get_by_id(cls, user_id):
        """Поиск пользователя по ID."""
        conn = get_db()
        cursor = conn.execute('''
            SELECT id, username, password, avatar, api_key
            FROM users
            WHERE id = ?
        ''', (user_id,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            return cls(**user_data)
        return None

    def save(self):
        """Сохраняет нового пользователя или обновляет существующего в базе данных."""
        try:
            with get_db() as conn:
                c = conn.cursor()
                if self.id is None:
                    c.execute('''
                        INSERT INTO users (username, password, avatar, api_key)
                        VALUES (?, ?, ?, ?)
                    ''', (self.username, self.password, self.avatar, self.api_key))
                    self.id = c.lastrowid  # Правильное использование
                else:
                    c.execute('''
                        UPDATE users
                        SET username = ?, password = ?, avatar = ?, api_key = ?
                        WHERE id = ?
                    ''', (self.username, self.password, self.avatar, self.api_key, self.id))
                conn.commit()
        except sqlite3.Error as e:
            print(f"[DB ERROR] Ошибка при сохранении пользователя: {e}")

    @classmethod
    def get_by_username(cls, username):
        """Поиск пользователя по имени пользователя."""
        conn = get_db()
        cursor = conn.execute('''
            SELECT id, username, password, avatar, api_key
            FROM users
            WHERE username = ?
        ''', (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            return cls(**user_data)
        return None

    @classmethod
    def get_by_api_key(cls, api_key):
        """Поиск пользователя по API ключу."""
        conn = get_db()
        cursor = conn.execute('''
            SELECT id, username, password, avatar, api_key
            FROM users
            WHERE api_key = ?
        ''', (api_key,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            return cls(**user_data)
        return None

    @classmethod
    def authenticate(cls, username, password):
        """Авторизация пользователя по имени и паролю."""
        user = cls.get_by_username(username)
        if user and user.password == password:
            return user
        return None


def get_db():
    """Получение подключения к базе данных с правильным путем."""
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../database/database.db')

    if not os.path.exists(db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Инициализация базы данных (создание таблиц)."""
    try:
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
            print("Database initialized and table created (if not already existing).")
    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")
