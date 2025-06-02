from functools import wraps
from flask import request, jsonify
from backend.utils.auth import verificar_token_jwt

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = None
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"message": "Token não fornecido"}), 401

        try:
            payload = verificar_token_jwt(token)
            request.usuario_id = int(payload.get("sub"))  # 🔧 conversão aqui
        except ValueError as e:
            return jsonify({"message": str(e)}), 401

        return f(*args, **kwargs)
    return decorated
