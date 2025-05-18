import os
from pathlib import Path
from dotenv import load_dotenv

class Config:
    def __init__(self):
        self.BASE_DIR = Path(__file__).parent.parent
        load_dotenv(self.BASE_DIR / '.env')
        
        # Обязательные параметры
        self.API_URL = os.getenv('API_URL', 'https://msk.apilk.tehno73.ru:8080/api')
        self.LS_NUM = os.getenv('LS_NUM')
        self.PASSWORD = os.getenv('PASSWORD')
        self.STORAGE_PATH = self.BASE_DIR / 'storage' / 'data.json'
        
        self._validate_config()

    def _validate_config(self):
        """Проверка обязательных параметров"""
        required = {
            'API_URL': self.API_URL,
            'LS_NUM': self.LS_NUM,
            'PASSWORD': self.PASSWORD
        }
        
        missing = [k for k, v in required.items() if not v]
        if missing:
            raise ValueError(f"Отсутствуют обязательные параметры: {', '.join(missing)}")