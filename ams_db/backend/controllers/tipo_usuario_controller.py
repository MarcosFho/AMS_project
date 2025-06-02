from flask import Blueprint, request, jsonify
from backend.schemas.tipo_usuario_schema import (
    TipoUsuarioCreateSchema, TipoUsuarioResponseSchema, TipoUsuarioUpdateSchema
)
from backend.services.tipo_usuario_service import (
    listar_tipos_usuario, buscar_tipo_usuario, criar_tipo_usuario,
    atualizar_tipo_usuario, deletar_tipo_usuario
)
from backend.middlewares.auth_middleware import auth_required

tipo_usuario_bp = Blueprint('tipo_usuario', __name__)

@tipo_usuario_bp.route("/tipos-usuario", methods=["GET"])
def get_tipos_usuario():
    tipos = listar_tipos_usuario()
    return jsonify([
        TipoUsuarioResponseSchema.model_validate(t).model_dump()
        for t in tipos
    ])

@tipo_usuario_bp.route("/tipos-usuario/<int:id>", methods=["GET"])
def get_tipo_usuario(id):
    tipo = buscar_tipo_usuario(id)
    if tipo:
        return jsonify(TipoUsuarioResponseSchema.model_validate(tipo).model_dump())
    return jsonify({"message": "Tipo de usuário não encontrado"}), 404

@tipo_usuario_bp.route("/tipos-usuario", methods=["POST"])
def post_tipo_usuario():
    dados = TipoUsuarioCreateSchema(**request.json)
    tipo = criar_tipo_usuario(dados.dict())
    return jsonify(TipoUsuarioResponseSchema.model_validate(tipo).model_dump()), 201

@tipo_usuario_bp.route("/tipos-usuario/<int:id>", methods=["PUT"])
@auth_required
def put_tipo_usuario(id):
    dados = TipoUsuarioUpdateSchema(**request.json)
    tipo = atualizar_tipo_usuario(id, dados.model_dump(exclude_unset=True))  # ✅ atualização parcial
    if tipo:
        return jsonify(TipoUsuarioResponseSchema.model_validate(tipo).model_dump())
    return jsonify({"message": "Tipo de usuário não encontrado"}), 404

@tipo_usuario_bp.route("/tipos-usuario/<int:id>", methods=["DELETE"])
@auth_required
def delete_tipo_usuario(id):
    tipo = deletar_tipo_usuario(id)
    if tipo:
        return jsonify({"message": "Tipo de usuário excluído com sucesso"})
    return jsonify({"message": "Tipo de usuário não encontrado"}), 404
