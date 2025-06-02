from flask import Blueprint, request, jsonify
from backend.schemas.endereco_schema import EnderecoCreateSchema, EnderecoResponseSchema, EnderecoUpdateSchema
from backend.services.endereco_service import (
    criar_endereco, buscar_endereco,
    atualizar_endereco, deletar_endereco
)
from backend.middlewares.auth_middleware import auth_required

endereco_bp = Blueprint('endereco', __name__)

# 🔹 Criar endereço
@endereco_bp.route("/enderecos", methods=["POST"])
def post_endereco():
    dados = EnderecoCreateSchema(**request.json)
    endereco = criar_endereco(dados.dict())
    resposta = EnderecoResponseSchema.model_validate(endereco).model_dump()
    return jsonify(resposta), 201

# 🔹 Buscar endereço por ID
@endereco_bp.route("/enderecos/<int:id>", methods=["GET"])
def get_endereco(id):
    endereco = buscar_endereco(id)
    if endereco:
        resposta = EnderecoResponseSchema.model_validate(endereco).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Endereço não encontrado"}), 404

# 🔹 Atualizar endereço
@endereco_bp.route("/enderecos/<int:id>", methods=["PUT"])
@auth_required
def put_endereco(id):
    dados = EnderecoUpdateSchema(**request.json)
    dados_dict = dados.dict(exclude_unset=True)
    endereco = atualizar_endereco(id, dados_dict)
    if endereco:
        resposta = EnderecoResponseSchema.model_validate(endereco).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Endereço não encontrado"}), 404

# 🔹 Excluir endereço
@endereco_bp.route("/enderecos/<int:id>", methods=["DELETE"])
@auth_required
def delete_endereco(id):
    endereco = deletar_endereco(id)
    if endereco:
        return jsonify({"message": "Endereço excluído com sucesso"})
    return jsonify({"message": "Endereço não encontrado"}), 404
