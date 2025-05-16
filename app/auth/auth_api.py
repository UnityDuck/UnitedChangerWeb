from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth.utils import generate_random_api_key
from app.db.models import User

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

    password_hash = generate_password_hash(password1, method='pbkdf2:sha256')
    api_key = generate_random_api_key()

    if User.get_by_username(username):
        return jsonify({"success": False, "error": "Пользователь уже существует"}), 409

    new_user = User(username=username, password=password_hash, api_key=api_key)
    new_user.save()

    return jsonify({"success": True, "message": "Регистрация успешна", "api_key": api_key}), 201


@auth_rest_api.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "error": "Имя пользователя и пароль обязательны"}), 400

    user = User.get_by_username(username)

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return jsonify({"success": True, "message": "Вход выполнен успешно", "api_key": user.api_key}), 200
    else:
        return jsonify({"success": False, "error": "Неверное имя пользователя или пароль"}), 401
