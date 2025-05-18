import json
from flask import current_app

def load_storage():
    """Загрузка данных из хранилища"""
    storage_path = current_app.config_object.STORAGE_PATH
    try:
        with open(storage_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_storage(data):
    """Сохранение данных в хранилище"""
    storage_path = current_app.config_object.STORAGE_PATH
    with open(storage_path, 'w') as f:
        json.dump(data, f, indent=2)