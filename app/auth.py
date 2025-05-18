import os
import requests
from datetime import datetime, timedelta
from app.config import Config
from app.utils import load_storage, save_storage

def get_auth_token():
    """Получение нового токена авторизации"""
    try:
        response = requests.post(
            f"{os.getenv('API_URL')}/Account/GetToken",
            json={"password": os.getenv('PASSWORD'), "lsNum": os.getenv('LS_NUM')},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        return {
            "auth_token": data['accessToken'],
            "token_expires": data['expiresDate']
        }
    except Exception as e:
        raise Exception(f"Auth error: {str(e)}")

def refresh_token():
    """Обновление токена с сохранением в хранилище"""
    try:
        token_data = get_auth_token()
        storage = load_storage()
        storage.update(token_data)
        save_storage(storage)
        return token_data['auth_token']
    except Exception as e:
        raise Exception(f"Token refresh failed: {str(e)}")