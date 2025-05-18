from flask import jsonify

def init_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Неверный запрос"}), 400
        
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": "Внутренняя ошибка сервера"}), 500