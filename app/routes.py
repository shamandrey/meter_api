from typing import List
from flask import Blueprint, jsonify, request, current_app
from datetime import datetime
from app.models import MeterResponse
from app.auth import get_auth_token, refresh_token
import requests
from app.utils import load_storage, save_storage

# Создаем Blueprint
api_blueprint = Blueprint('api', __name__, url_prefix='/api')


@api_blueprint.route('/meters', methods=['GET'])
def get_meters() -> MeterResponse:
    """
    Получает список счетчиков из API WirenBoard
    Возвращает:
        tuple: (JSON-ответ, HTTP-статус)
    """
    try:
        
        storage = load_storage()

        # Получаем/обновляем токен
        if not storage.get('auth_token'):
            refresh_token()
            save_storage(storage)

        # Запрос к API
        response = requests.post(
            f"{current_app.config_object.API_URL}/LkUser/GetLsMeterList",
            headers=_get_auth_headers(storage),
            timeout=15,
            json={}
        )
        # Обработка ответа
        if response.status_code == 200:
            # meters = _parse_meters_response(response.json())
            # print(meters[0])
            return jsonify(response.json()), 200

        elif response.status_code == 404:
            print(123344)
        elif response.status_code == 401:
            refresh_token()
            return get_meters()  # Retry with new token
        print(123344)
        return jsonify({'error': 'API недоступен'}), 502

    except Exception as e:
        current_app.logger.error(f"Ошибка: {str(e)}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500

@api_blueprint.route('/submit', methods=['POST'])
def submit_reading():
    """Отправка показаний"""
    try:
        storage = load_storage()
        data = request.json
        if not data or 'meterID' not in data or 'value' not in data:
            return jsonify({"error": "Требуются meterID и value"}), 400
        meters, ststus = get_meters()
        responceData: MeterResponse = meters.get_json()
        curentMeter = [meter for meter in responceData['getLkMeterItems'] if meter['meterID'] == data['meterID']]
        if curentMeter.__len__() == 0:
            return jsonify({"error": "Такого счетсика несуществует"}), 400
        
        if ststus != 200:
            return jsonify({"error": "Не получилось запросить сщетчики"})

        if curentMeter[0]['meterID'] == data['meterID']:
            if curentMeter[0]['currentValue'] > data['value']:
                data['value'] = curentMeter[0]['currentValue']
        storage = load_storage()
        if not storage.get('auth_token'):
            token_data = get_auth_token()
            storage.update(token_data)
            save_storage(storage)

        response = requests.post(
            f"{current_app.config_object.API_URL}/LkUser/AddMeterage",
            headers={
                "Authorization": f"Bearer {storage['auth_token']}",
                "Content-Type": "application/json"
            },
            json={
                "meterID": int(data['meterID']),
                "newValue": float(data['value'])
            },
            timeout=10
        )

        if response.status_code == 200:
            return jsonify({"status": "success"})
        elif response.status_code == 401:
            refresh_token()
            return submit_reading()  # Повторная попытка
        else:
            return jsonify({"error": f"API error: {response.status_code}"}), 502

    except ValueError:
        return jsonify({"error": "Неверный формат данных"}), 400
    except Exception as e:
        current_app.logger.error(f"Error in submit_reading: {str(e)}")
        return jsonify({"error": str(e)}), 500

def _get_auth_headers(storage: dict) -> dict:
    """Возвращает заголовки авторизации"""
    return {
        "Authorization": f"Bearer {storage['auth_token']}",
        "Content-Type": "application/json"
    }

# Экспортируем Blueprint для использования в __init__.py
__all__ = ['api_blueprint']