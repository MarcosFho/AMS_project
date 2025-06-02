from flask import jsonify
from pydantic import ValidationError

def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({"erro": e.errors()}), 400

    @app.errorhandler(400)
    def erro_400(e):
        return jsonify({"erro": "Requisição inválida"}), 400

    @app.errorhandler(404)
    def erro_404(e):
        return jsonify({"erro": "Recurso não encontrado"}), 404

    @app.errorhandler(413)
    def erro_413(e):
        return jsonify({"erro": "Arquivo excede o tamanho máximo permitido (2MB)"}), 413

    @app.errorhandler(500)
    def erro_500(e):
        return jsonify({"erro": "Erro interno do servidor"}), 500
