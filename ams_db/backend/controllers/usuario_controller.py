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
from backend.models.prestador_model import Prestador
from backend.config.session import get_db
from backend.middlewares.auth_middleware import auth_required
import os

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route("/usuarios", methods=["POST"])
def post_usuario():
    try:
        if request.is_json:
            dados_dict = request.get_json()
        else:
            dados_dict = request.form.to_dict()
            if "endereco_id" in dados_dict:
                dados_dict["id_endereco"] = dados_dict.pop("endereco_id")
        # Garante id_endereco correto
        if "id_endereco" in dados_dict and dados_dict["id_endereco"] == "":
            dados_dict["id_endereco"] = None
        elif "id_endereco" in dados_dict:
            dados_dict["id_endereco"] = int(dados_dict["id_endereco"])

        dados = UsuarioCreateSchema(**dados_dict)
    except Exception as e:
        return jsonify({"erro": "Dados inválidos", "detalhes": str(e)}), 400

    dados_dict = dados.dict()
    tipo_nome = dados_dict.pop("tipo_usuario", "").upper()
    senha_plana = dados_dict.pop("senha")

    usuario_fields = ["nome", "email", "telefone", "foto_url", "id_endereco", "tipo_usuario_id", "status"]
    usuario_data = {field: dados_dict.get(field) for field in usuario_fields if field in dados_dict}

    with get_db() as db:
        tipo = db.query(TipoUsuario).filter(TipoUsuario.nome == tipo_nome).first()
        if not tipo:
            return jsonify({"message": "Tipo de usuário inválido"}), 400

        if db.query(Usuario).filter(Usuario.email == dados_dict["email"]).first():
            return jsonify({"message": "Email já cadastrado"}), 409

        usuario_data["tipo_usuario_id"] = tipo.id

        foto = request.files.get("foto")
        if foto:
            pasta_fotos = "static/uploads/fotos_usuarios"
            os.makedirs(pasta_fotos, exist_ok=True)
            extensao = os.path.splitext(foto.filename)[1]
            nome_arquivo = f"{dados_dict['email'].replace('@', '_')}{extensao}"
            caminho_foto = os.path.join(pasta_fotos, nome_arquivo)
            foto.save(caminho_foto)
            # >>>>> Corrige o caminho salvo no banco <<<<<
            # Caminho relativo a partir de 'uploads'
            relative_path = os.path.relpath(caminho_foto, "static/uploads").replace(os.sep, "/")
            usuario_data["foto_url"] = relative_path

        usuario = Usuario(**usuario_data)
        db.add(usuario)
        db.flush()
        db.refresh(usuario)

        criar_login({
            "id_usuario": usuario.id,
            "senha_hash": gerar_hash_senha(senha_plana)
        }, db=db)

        # Se for PRESTADOR, cria o registro na tabela prestador
        if tipo_nome == "PRESTADOR":
            categoria = request.form.get("categoria", "")
            localizacao = request.form.get("localizacao", "")
            prestador = Prestador(
                id_usuario=usuario.id,
                categoria=categoria,
                localizacao=localizacao
            )
            db.add(prestador)
            db.flush()

        db.commit()
        resposta = UsuarioResponseSchema.model_validate(usuario).model_dump()
        return jsonify(resposta), 201

@usuario_bp.route("/usuarios", methods=["GET"])
def get_usuarios():
    usuarios = listar_usuarios()
    return jsonify([UsuarioResponseSchema.model_validate(u).model_dump() for u in usuarios])

@usuario_bp.route("/usuarios/<int:id>", methods=["GET"])
def get_usuario(id):
    usuario = buscar_usuario(id)
    if usuario:
        return jsonify(UsuarioResponseSchema.model_validate(usuario).model_dump())
    return jsonify({"message": "Usuário não encontrado"}), 404

@usuario_bp.route("/usuarios/<int:id>", methods=["PUT"])
@auth_required
def put_usuario(id):
    # Verifica se é multipart (com foto)
    if request.content_type and "multipart/form-data" in request.content_type:
        dados_dict = request.form.to_dict()
        foto = request.files.get("foto")
    else:
        try:
            dados = UsuarioUpdateSchema(**request.json)
            dados_dict = dados.model_dump(exclude_unset=True)
            foto = None
        except Exception as e:
            return jsonify({"erro": "Dados inválidos", "detalhes": str(e)}), 400

    # Trata id_endereco (caso venha do React)
    if "endereco_id" in dados_dict:
        dados_dict["id_endereco"] = dados_dict.pop("endereco_id")

    # Se tiver arquivo de foto, salva e atualiza foto_url
    if foto and foto.filename:
        pasta_fotos = "static/uploads/fotos_usuarios"
        os.makedirs(pasta_fotos, exist_ok=True)
        extensao = os.path.splitext(foto.filename)[1]
        nome_arquivo = f"usuario_{id}{extensao}"
        caminho_foto = os.path.join(pasta_fotos, nome_arquivo)
        foto.save(caminho_foto)
        # >>>>> Corrige o caminho salvo no banco <<<<<
        relative_path = os.path.relpath(caminho_foto, "static/uploads").replace(os.sep, "/")
        dados_dict["foto_url"] = relative_path


    resposta = atualizar_usuario(id, dados_dict)
    if resposta:
        return jsonify(resposta)
    return jsonify({"message": "Usuário não encontrado"}), 404

@usuario_bp.route("/usuarios/<int:id>", methods=["DELETE"])
@auth_required
def delete_usuario(id):
    usuario = deletar_usuario(id)
    if usuario:
        return jsonify({"message": "Usuário excluído com sucesso"})
    return jsonify({"message": "Usuário não encontrado"}), 404

@usuario_bp.route("/usuarios/perfil", methods=["GET", "OPTIONS"])
@auth_required
def perfil_usuario():
    usuario_id = request.usuario_id
    return jsonify({"mensagem": f"Usuário autenticado: {usuario_id}"}), 200

@usuario_bp.route("/usuarios/me", methods=["GET", "OPTIONS"])
@auth_required
def usuario_me():
    usuario_id = request.usuario_id
    usuario = buscar_usuario(usuario_id)
    if usuario:
        resposta = UsuarioResponseSchema.model_validate(usuario).model_dump()
        # Ajuste definitivo: remove barras à esquerda
        if resposta.get("foto_url"):
            resposta["foto_url"] = resposta["foto_url"].lstrip("/")
        return jsonify(resposta)
    return jsonify({"message": "Usuário não encontrado"}), 404

