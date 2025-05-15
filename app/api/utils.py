from app.db.models import get_db

def verify_api_key(api_key):
    """Проверка существования API ключа в базе данных."""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE api_key = ?', (api_key,))
    return True if c.fetchone() else False
