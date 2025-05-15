import random
import string

def generate_random_api_key():
    """Генерация случайного ключа API длиной 13 символов."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=13))
