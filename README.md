# Meter Readings API

## Установка
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Запуск
```bash
export FLASK_APP=app/main.py
flask run
```

## API Endpoints
- `GET /api/meters` - список счетчиков
- `POST /api/submit` - отправить показания