import os
import random
import string
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def init_db():
    with sqlite3.connect('database.db') as conn:
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


init_db()


def generate_random_api_key():
    """Генерация случайного ключа API длиной 13 символов."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=13))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form['username']:
            username = request.form['username']
            password1 = request.form['password']
            password = generate_password_hash(request.form['password'])
            confirm_password = request.form['confirm_password']

            if len(password) < 6:
                flash('Пароль должен быть не менее 6 символов', 'error')
                return render_template('register.html')

            if password1 != confirm_password:
                flash('Пароли не совпадают!', 'error')
                return render_template('register.html')

            with sqlite3.connect('database.db') as conn:
                c = conn.cursor()
                try:
                    api_key = generate_random_api_key()
                    c.execute('INSERT INTO users (username, password, api_key) VALUES (?, ?, ?)', (username, password, api_key))
                    conn.commit()
                    flash('Регистрация успешна! Пожалуйста, войдите в свой аккаунт.', 'success')
                    return redirect(url_for('login'))
                except sqlite3.IntegrityError:
                    flash('Пользователь с таким именем уже существует!', 'error')
                    return render_template('register.html')
    return render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE username=?', (username,))
            user = c.fetchone()
            if user and check_password_hash(user[2], password):
                session['user_id'] = user[0]
                flash('Успешный вход!', 'success')
                return redirect(url_for('profile'))
            else:
                flash('Неверное имя пользователя или пароль', 'error')
                return render_template('login.html')
    return render_template('login.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']

    if request.method == 'POST':
        file = request.files['avatar']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            with sqlite3.connect('database.db') as conn:
                c = conn.cursor()
                c.execute('UPDATE users SET avatar = ? WHERE id = ?', (filepath, user_id))
                conn.commit()
            flash('Аватар обновлён!')
            return redirect(url_for('profile'))

    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT avatar, api_key FROM users WHERE id = ?', (user_id,))
        avatar_path, api_key = c.fetchone()
        avatar_path = avatar_path or 'static/default.png'

    return render_template('profile.html', avatar=avatar_path, api_key=api_key)


@app.route('/generate_api_key', methods=['GET', 'POST'])
def generate_api_key():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        new_api_key = generate_random_api_key()
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('UPDATE users SET api_key = ? WHERE id = ?', (new_api_key, user_id))
            conn.commit()
        return {'api_key': new_api_key}

    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT avatar, api_key FROM users WHERE id = ?', (user_id,))
        avatar_path, api_key = c.fetchone()
        avatar_path = avatar_path or 'static/default.png'

    return render_template('generate_api_key.html', avatar=avatar_path, api_key=api_key)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Вы вышли из аккаунта.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
