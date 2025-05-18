from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    
    # Инициализация конфигурации
    try:
        app.config_object = Config()
    except Exception as e:
        app.logger.error(f"Configuration error: {str(e)}")
        raise
    
    # Регистрация Blueprint
    from .routes import api_blueprint
    app.register_blueprint(api_blueprint)
    
    return app