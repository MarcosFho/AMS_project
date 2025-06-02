from flask import Blueprint, request, jsonify
from backend.schemas.login_schema import (
    LoginCreateSchema, LoginResponseSchema, LoginAuthSchema,
    TokenSchema, LoginUpdateSchema
)
from backend.services.login_service import (
    criar_login, buscar_login_por_usuario, atualizar_ultimo_login,
    autenticar_usuario, redefinir_senha, ativar_usuario, atualizar_login
)
from backend.utils.auth import gerar_token_jwt, verificar_token_jwt
from backend.utils.crypto import gerar_hash_senha

login_bp = Blueprint('login', __name__)

# 🔹 Criar login
@login_bp.route("/api/logins", methods=["POST"])
def post_login():
    try:
        dados = LoginCreateSchema(**request.json)
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

    dados_dict = dados.dict()
    dados_dict["senha_hash"] = gerar_hash_senha(dados_dict.pop("senha"))

    login = criar_login(dados_dict)
    resposta = LoginResponseSchema.model_validate(login).model_dump()
    return jsonify(resposta), 201

# 🔹 Buscar login por ID de usuário
@login_bp.route("/api/logins/<int:id_usuario>", methods=["GET"])
def get_login(id_usuario):
    login = buscar_login_por_usuario(id_usuario)
    if login:
        resposta = LoginResponseSchema.model_validate(login).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Login não encontrado"}), 404

# 🔹 Atualizar login parcialmente
@login_bp.route("/api/logins/<int:id_usuario>", methods=["PUT"])
def put_login(id_usuario):
    try:
        dados = LoginUpdateSchema(**request.json)
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

    login = atualizar_login(id_usuario, dados.model_dump(exclude_unset=True))
    if login:
        resposta = LoginResponseSchema.model_validate(login).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Login não encontrado"}), 404

# 🔹 Atualizar último login
@login_bp.route("/api/logins/<int:id_usuario>/ultimo-login", methods=["PUT"])
def put_ultimo_login(id_usuario):
    login = atualizar_ultimo_login(id_usuario)
    if login:
        return jsonify({"message": "Último login atualizado"}), 200
    return jsonify({"message": "Login não encontrado"}), 404

# 🔹 Autenticar usuário e retornar token
@login_bp.route("/api/login/autenticar", methods=["POST"])
def autenticar_login():
    try:
        dados = LoginAuthSchema(**request.json)
        token = autenticar_usuario(dados.email, dados.senha)
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

    if token:
        return jsonify({"access_token": token}), 200
    return jsonify({"message": "Credenciais inválidas"}), 401

# 🔹 Iniciar recuperação de senha (gera token)
@login_bp.route("/api/login/recuperar", methods=["POST"])
def recuperar_senha():
    dados = request.json
    id_usuario = dados.get("id_usuario")
    if not id_usuario:
        return jsonify({"message": "Informe o ID do usuário"}), 400

    token = gerar_token_jwt({"sub": str(id_usuario)}, exp_minutes=15)
    return jsonify({"token_recuperacao": token}), 200

# 🔹 Redefinir senha com token de recuperação
@login_bp.route("/api/login/redefinir", methods=["POST"])
def redefinir_senha_route():
    dados = request.json
    token = dados.get("token")
    nova_senha = dados.get("nova_senha")

    if not token or not nova_senha:
        return jsonify({"message": "Token e nova senha são obrigatórios"}), 400

    try:
        payload = verificar_token_jwt(token)
        id_usuario = int(payload.get("sub"))
    except Exception as e:
        return jsonify({"message": f"Token inválido: {e}"}), 401

    senha_hash = gerar_hash_senha(nova_senha)
    redefinir_senha(id_usuario, senha_hash)
    return jsonify({"message": "Senha redefinida com sucesso"}), 200

# 🔹 Gerar token de ativação
@login_bp.route("/api/login/ativar/gerar", methods=["POST"])
def gerar_token_ativacao():
    dados = request.json
    id_usuario = dados.get("id_usuario")
    if not id_usuario:
        return jsonify({"message": "ID de usuário é obrigatório"}), 400

    token = gerar_token_jwt({"sub": str(id_usuario)}, exp_minutes=30)
    link = f"http://localhost:5000/login/ativar/{token}"
    return jsonify({"link_ativacao": link}), 200

# 🔹 Validar token e ativar usuário
@login_bp.route("/api/login/ativar/<token>", methods=["GET"])
def ativar_usuario_token(token):
    try:
        payload = verificar_token_jwt(token)
        id_usuario = int(payload.get("sub"))
        ativar_usuario(id_usuario)
        return jsonify({"message": "Usuário ativado com sucesso"}), 200
    except Exception as e:
        return jsonify({"message": f"Token inválido: {e}"}), 401

# 🔹 Alias para autenticar também via /login
@login_bp.route("/api/login", methods=["POST"])
def login_alias():
    return autenticar_login()
