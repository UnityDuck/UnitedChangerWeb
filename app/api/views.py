import os
from datetime import datetime
import sqlite3
from flask import Blueprint, jsonify, request
import requests

from app.api.utils import verify_api_key
from app.db.models import User

api_services = Blueprint('api_services', __name__)

TRADERMADE_API_KEY = 'eGCvr06hXSw0oinclXKs'
TRADERMADE_API_URL = 'https://marketdata.tradermade.com/api/v1/timeseries'


@api_services.route('/api/rate', methods=['GET'])
def get_currency_rate():
    """
    Получить текущий курс валюты.
    Пример запроса:
    GET /api/rate?from=USD&to=EUR&api_key=ВАШ_КЛЮЧ

    :return: обменный курс между двумя валютами
    """
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    api_key = request.args.get('api_key')

    if not verify_api_key(api_key):
        return jsonify({"error": "Неверный API ключ"}), 403

    if not from_currency or not to_currency:
        return jsonify({"error": "Missing 'from' or 'to' parameter"}), 400

    url = f'https://api.coinbase.com/v2/exchange-rates?currency={from_currency}'
    response = requests.get(url)
    data = response.json()

    if 'data' not in data or to_currency not in data['data']['rates']:
        return jsonify({"error": "Currency not found"}), 404

    rate = data['data']['rates'][to_currency]
    return jsonify({"rate": rate})


@api_services.route('/api/ohlc', methods=['GET'])
def get_historical_data():
    """
    Получить исторические данные OHLC для валютной пары.
    Пример запроса:
    GET /api/ohlc?currency=EURUSD&start_date=2024-05-01&end_date=2024-05-14&api_key=ВАШ_КЛЮЧ

    :return: исторические данные OHLC
    """
    currency_pair = request.args.get('currency')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    user_api_key = request.args.get('api_key')

    if not all([currency_pair, start_date, end_date, user_api_key]):
        return jsonify({'success': False, 'error': 'currency, start_date, end_date и api_key обязательны'}), 400

    user = User.get_by_api_key(user_api_key)
    if not user:
        return jsonify({'success': False, 'error': 'Неверный API ключ'}), 403

    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'success': False, 'error': 'Неверный формат даты. Используйте YYYY-MM-DD'}), 400

    params = {
        'currency': currency_pair,
        'start_date': start_date,
        'end_date': end_date,
        'format': 'records',
        'api_key': TRADERMADE_API_KEY
    }

    try:
        response = requests.get(TRADERMADE_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get('success'):
            return jsonify({'success': True, 'error': 'None', 'details': data}), 200

        ohlc_data = data.get('data', [])
        return jsonify({
            'success': True,
            'symbol': data.get('symbol', currency_pair),
            'start_date': start_date,
            'end_date': end_date,
            'records': ohlc_data
        }), 200

    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'error': str(e)}), 500
