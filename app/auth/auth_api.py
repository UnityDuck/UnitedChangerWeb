from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

from app.auth.utils import generate_random_api_key
from app.db.models import get_db

auth_rest_api = Blueprint('auth_rest_api', __name__, url_prefix="/rest")


@auth_rest_api.route('/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data.get('username')
    password1 = data.get('password')
    confirm_password = data.get('confirm_password')

    if not username or not password1 or not confirm_password:
        return jsonify({"success": False, "error": "Все поля обязательны"}), 400

    if len(password1) < 6:
        return jsonify({"success": False, "error": "Пароль должен быть не менее 6 символов"}), 400

    if password1 != confirm_password:
        return jsonify({"success": False, "error": "Пароли не совпадают"}), 400

    password_hash = generate_password_hash(password1)
    api_key = generate_random_api_key()

    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password, api_key) VALUES (?, ?, ?)', (username, password_hash, api_key))
        conn.commit()
        return jsonify({"success": True, "message": "Регистрация успешна", "api_key": api_key}), 201
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "error": "Пользователь уже существует"}), 409


@auth_rest_api.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "error": "Имя пользователя и пароль обязательны"}), 400

    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, password, api_key FROM users WHERE username = ?', (username,))
    user = c.fetchone()

    if user and check_password_hash(user[1], password):
        session['user_id'] = user[0]
        return jsonify({"success": True, "message": "Вход выполнен успешно", "api_key": user[2]}), 200
    else:
        return jsonify({"success": False, "error": "Неверное имя пользователя или пароль"}), 401
