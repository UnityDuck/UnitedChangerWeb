import os
import sqlite3

from flask import Blueprint, jsonify, request, redirect, url_for, session, flash, render_template
from werkzeug.utils import secure_filename
import requests

from app.auth.utils import generate_random_api_key
from app.db.models import User
from app.api.utils import verify_api_key

api_bp = Blueprint('api', __name__)


@api_bp.route('/exchange_rate', methods=['GET'])
def exchange_rate():
    api_key = request.args.get('api_key')
    base_currency = request.args.get('base', 'USD').upper()
    target_currency = request.args.get('target', 'EUR').upper()

    if not verify_api_key(api_key):
        return jsonify({'success': False, 'error': 'Неверный API ключ'}), 403

    try:
        url = f"https://api.coinbase.com/v2/exchange-rates?currency={base_currency}"
        response = requests.get(url)
        data = response.json()

        rate = data['data']['rates'].get(target_currency)
        if not rate:
            return jsonify({'success': False, 'error': 'Неверная валюта'}), 400

        return jsonify({
            'success': True,
            'base': base_currency,
            'target': target_currency,
            'rate': rate
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/generate_api_key', methods=['GET', 'POST'])
def generate_api_key():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    if request.method == 'POST':
        action = request.form.get('action')
        if action == "upload_avatar":
            file = request.files['avatar']
            if file:
                filename = secure_filename(file.filename)
                parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                upload_folder = os.path.join(parent_dir, 'static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                relative_filepath = os.path.join('uploads', filename)

                user = User.get_by_id(user_id)
                if user:
                    user.avatar = relative_filepath
                    user.save()

                flash('Аватар обновлён!')
                return redirect(url_for('api.generate_api_key'))

        elif action == "generate_key":
            new_key = generate_random_api_key()
            user = User.get_by_id(user_id)
            if user:
                user.api_key = new_key
                user.save()
            flash('API-ключ успешно сгенерирован!')
            return redirect(url_for('api.generate_api_key'))

    user = User.get_by_id(user_id)
    if user:
        avatar_path = user.avatar or 'default.png'
        return render_template('generate_api_key.html', avatar=f"../static/{avatar_path}", api_key=user.api_key)
    return redirect(url_for('auth.login'))


@api_bp.route('/docs', methods=['GET', 'POST'])
def docs():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

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

            user = User.get_by_id(user_id)
            if user:
                user.avatar = relative_filepath
                user.save()

            flash('Аватар обновлён!')
            return redirect(url_for('api.docs'))

    user = User.get_by_id(user_id)
    if user:
        avatar_path = user.avatar or 'default.png'
        return render_template('docs.html', avatar=f"../static/{avatar_path}", api_key=user.api_key)
    return redirect(url_for('auth.login'))


api_generator = Blueprint("api_generator", __name__)


@api_generator.route('/generate_api_key', methods=['POST'])
def generate_api_key():
    """Обработчик для генерации API-ключа и его сохранения в базе данных."""
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    api_key = generate_random_api_key()

    try:
        user = User.get_by_id(user_id)
        if user:
            user.api_key = api_key
            user.save()

        return jsonify({"api_key": api_key}), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
