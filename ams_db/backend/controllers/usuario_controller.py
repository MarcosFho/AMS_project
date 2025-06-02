from flask import Blueprint, request, jsonify
from backend.schemas.usuario_schema import (
    UsuarioCreateSchema,
    UsuarioResponseSchema,
    UsuarioUpdateSchema
)
from backend.services.usuario_service import (
    listar_usuarios, buscar_usuario, atualizar_usuario, deletar_usuario
)
from backend.services.login_service import criar_login
from backend.utils.crypto import gerar_hash_senha
from backend.models.tipo_usuario_model import TipoUsuario
from backend.models.usuario_model import Usuario
from backend.config.session import get_db
from backend.middlewares.auth_middleware import auth_required
import os

usuario_bp = Blueprint('usuario', __name__)

# 🔹 Criar um novo usuário com login
@usuario_bp.route("/api/usuarios", methods=["POST"])
def post_usuario():
    try:
        form_data = request.form.to_dict()
        if "endereco_id" in form_data and form_data["endereco_id"] == "":
            form_data["endereco_id"] = None
        elif "endereco_id" in form_data:
            form_data["endereco_id"] = int(form_data["endereco_id"])
        
        dados = UsuarioCreateSchema(**form_data)
    except Exception as e:
        return jsonify({"erro": "Dados inválidos", "detalhes": str(e)}), 400

    dados_dict = dados.dict()
    tipo_nome = dados_dict.pop("tipo_usuario", "").upper()
    senha_plana = dados_dict.pop("senha")

    with get_db() as db:
        # 🔸 Verifica se o tipo de usuário é válido
        tipo = db.query(TipoUsuario).filter(TipoUsuario.nome == tipo_nome).first()
        if not tipo:
            return jsonify({"message": "Tipo de usuário inválido"}), 400

        # 🔸 Verifica se o e-mail já está em uso
        if db.query(Usuario).filter(Usuario.email == dados_dict["email"]).first():
            return jsonify({"message": "Email já cadastrado"}), 409

        # 🔸 Corrige campo endereco_id → id_endereco (como esperado pelo model)
        if "endereco_id" in dados_dict:
            dados_dict["id_endereco"] = dados_dict.pop("endereco_id")

        dados_dict["tipo_usuario_id"] = tipo.id

        # 🔸 Upload de foto (opcional)
        foto = request.files.get("foto")
        if foto:
            pasta_fotos = "static/uploads/fotos_usuarios"
            os.makedirs(pasta_fotos, exist_ok=True)
            extensao = os.path.splitext(foto.filename)[1]
            nome_arquivo = f"{dados_dict['email'].replace('@', '_')}{extensao}"
            caminho_foto = os.path.join(pasta_fotos, nome_arquivo)
            foto.save(caminho_foto)
            dados_dict["foto_url"] = f"/{caminho_foto.replace(os.sep, '/')}"

        # 🔸 Cria o usuário
        usuario = Usuario(**dados_dict)
        db.add(usuario)
        db.flush()
        db.refresh(usuario)

        # 🔸 Cria o login com senha hasheada
        criar_login({
            "id_usuario": usuario.id,
            "senha_hash": gerar_hash_senha(senha_plana)
        }, db=db)

        db.commit()

        resposta = UsuarioResponseSchema.model_validate(usuario).model_dump()
        return jsonify(resposta), 201


# 🔹 Listar todos os usuários
@usuario_bp.route("/api/usuarios", methods=["GET"])
def get_usuarios():
    usuarios = listar_usuarios()
    return jsonify([UsuarioResponseSchema.model_validate(u).model_dump() for u in usuarios])


# 🔹 Buscar usuário por ID
@usuario_bp.route("/api/usuarios/<int:id>", methods=["GET"])
def get_usuario(id):
    usuario = buscar_usuario(id)
    if usuario:
        return jsonify(UsuarioResponseSchema.model_validate(usuario).model_dump())
    return jsonify({"message": "Usuário não encontrado"}), 404


# 🔹 Atualizar usuário por ID
@usuario_bp.route("/api/usuarios/<int:id>", methods=["PUT"])
@auth_required
def put_usuario(id):
    try:
        dados = UsuarioUpdateSchema(**request.json)
    except Exception as e:
        return jsonify({"erro": "Dados inválidos", "detalhes": str(e)}), 400

    dados_dict = dados.model_dump(exclude_unset=True)

    # Corrige o nome do campo se vier do frontend
    if "endereco_id" in dados_dict:
        dados_dict["id_endereco"] = dados_dict.pop("endereco_id")

    usuario = atualizar_usuario(id, dados_dict)
    if usuario:
        return jsonify(UsuarioResponseSchema.model_validate(usuario).model_dump())
    return jsonify({"message": "Usuário não encontrado"}), 404


# 🔹 Excluir usuário por ID
@usuario_bp.route("/api/usuarios/<int:id>", methods=["DELETE"])
@auth_required
def delete_usuario(id):
    usuario = deletar_usuario(id)
    if usuario:
        return jsonify({"message": "Usuário excluído com sucesso"})
    return jsonify({"message": "Usuário não encontrado"}), 404


# 🔹 Perfil autenticado
@usuario_bp.route("/api/usuarios/perfil", methods=["GET"])
@auth_required
def perfil_usuario():
    usuario_id = request.usuario_id
    return jsonify({"mensagem": f"Usuário autenticado: {usuario_id}"}), 200

# 🔹 Obter dados do usuário autenticado
@usuario_bp.route("/api/usuarios/me", methods=["GET"])
@auth_required
def get_usuario_autenticado():
    usuario_id = request.usuario_id

    with get_db() as db:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        return jsonify(UsuarioResponseSchema.model_validate(usuario).model_dump()), 200
