from flask import Blueprint, request, jsonify
from backend.schemas.loja_schema import (
    LojaCreateSchema, LojaResponseSchema, LojaUpdateSchema
)
from backend.services.loja_service import (
    criar_loja, listar_lojas, buscar_loja,
    atualizar_loja, deletar_loja
)
from backend.middlewares.auth_middleware import auth_required

loja_bp = Blueprint('loja', __name__)

# 🔹 Criar nova loja
@loja_bp.route("/lojas", methods=["POST"])
def post_loja():
    dados = LojaCreateSchema(**request.json)
    dados_dict = dados.dict()
    dados_dict["id_usuario"] = int(request.usuario_id)  # associa ao usuário autenticado

    loja = criar_loja(dados_dict)
    resposta = LojaResponseSchema.model_validate(loja).model_dump()
    return jsonify(resposta), 201

# 🔹 Listar todas as lojas
@loja_bp.route("/lojas", methods=["GET"])
def get_lojas():
    lojas = listar_lojas()
    return jsonify([
        LojaResponseSchema.model_validate(l).model_dump()
        for l in lojas
    ])

# 🔹 Buscar loja por ID
@loja_bp.route("/lojas/<int:id>", methods=["GET"])
def get_loja(id):
    loja = buscar_loja(id)
    if loja:
        resposta = LojaResponseSchema.model_validate(loja).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Loja não encontrada"}), 404

# 🔹 Atualizar loja por ID
@loja_bp.route("/lojas/<int:id>", methods=["PUT"])
@auth_required
def put_loja(id):
    dados = LojaUpdateSchema(**request.json)
    dados_dict = dados.dict(exclude_unset=True)
    loja = atualizar_loja(id, dados_dict)
    if loja:
        resposta = LojaResponseSchema.model_validate(loja).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Loja não encontrada"}), 404

# 🔹 Excluir loja por ID
@loja_bp.route("/lojas/<int:id>", methods=["DELETE"])
@auth_required
def delete_loja(id):
    loja = deletar_loja(id)
    if loja:
        return jsonify({"message": "Loja excluída com sucesso"})
    return jsonify({"message": "Loja não encontrada"}), 404
