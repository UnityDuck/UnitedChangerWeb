import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from app.auth.utils import generate_random_api_key
from app.db.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password']
        password = generate_password_hash(password1, method='pbkdf2:sha256')
        confirm_password = request.form['confirm_password']

        if len(password) < 6:
            flash('Пароль должен быть не менее 6 символов', 'error')
            return render_template('register.html')

        if password1 != confirm_password:
            flash('Пароли не совпадают!', 'error')
            return render_template('register.html')

        if User.get_by_username(username):
            flash('Пользователь с таким именем уже существует!', 'error')
            return render_template('register.html')

        api_key = generate_random_api_key()
        new_user = User(username=username, password=password, api_key=api_key)
        new_user.save()

        flash('Регистрация успешна! Пожалуйста, войдите в свой аккаунт.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route("/", methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.get_by_username(username)
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Успешный вход!', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')
            return render_template('login.html')
    return render_template('login.html')


@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    user = User.get_by_id(user_id)
    if not user:
        flash('Пользователь не найден.', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        file = request.files['avatar']
        if file:
            filename = secure_filename(file.filename)
            parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            upload_folder = os.path.join(parent_dir, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            relative_filepath = os.path.join('uploads', filename)
            user.avatar = relative_filepath
            user.save()
            flash('Аватар обновлён!')
            return redirect(url_for('auth.profile'))

    avatar_path = user.avatar or 'default.png'
    return render_template('profile.html', avatar=f"static/{avatar_path}", api_key=user.api_key)


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Вы вышли из аккаунта.', 'info')
    return redirect(url_for('auth.login'))
