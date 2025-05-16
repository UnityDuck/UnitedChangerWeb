from app.db.models import User


def verify_api_key(api_key):
    """Проверка существования API ключа в базе данных."""
    user = User.get_by_api_key(api_key)
    return True if user else False
