from flask import Blueprint, request, jsonify
from backend.schemas.trabalhe_conosco_schema import TrabalheConoscoCreateSchema, TrabalheConoscoResponseSchema
from backend.services.trabalhe_conosco_service import (
    criar_trabalhe_conosco, listar_trabalhe_conosco,
    buscar_trabalhe_conosco, deletar_trabalhe_conosco
)
from backend.middlewares.auth_middleware import auth_required

trabalhe_conosco_bp = Blueprint('trabalhe_conosco', __name__)

# 🔹 Criar uma nova inscrição Trabalhe Conosco
@trabalhe_conosco_bp.route("/trabalhe-conosco", methods=["POST"])
def post_trabalhe_conosco():
    dados = TrabalheConoscoCreateSchema(**request.json)
    cadastro = criar_trabalhe_conosco(dados.dict())
    resposta = TrabalheConoscoResponseSchema.model_validate(cadastro).model_dump()
    return jsonify(resposta), 201

# 🔹 Listar todas as inscrições Trabalhe Conosco
@trabalhe_conosco_bp.route("/trabalhe-conosco", methods=["GET"])
def get_trabalhe_conosco():
    cadastros = listar_trabalhe_conosco()
    resposta = [TrabalheConoscoResponseSchema.model_validate(c).model_dump() for c in cadastros]
    return jsonify(resposta)

# 🔹 Buscar uma inscrição Trabalhe Conosco por ID
@trabalhe_conosco_bp.route("/trabalhe-conosco/<int:id>", methods=["GET"])
def get_trabalhe_conosco_id(id):
    cadastro = buscar_trabalhe_conosco(id)
    if cadastro:
        resposta = TrabalheConoscoResponseSchema.model_validate(cadastro).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Inscrição não encontrada"}), 404

# 🔹 Excluir uma inscrição Trabalhe Conosco por ID
@trabalhe_conosco_bp.route("/trabalhe-conosco/<int:id>", methods=["DELETE"])
@auth_required
def delete_trabalhe_conosco(id):
    cadastro = deletar_trabalhe_conosco(id)
    if cadastro:
        return jsonify({"message": "Inscrição excluída com sucesso"})
    return jsonify({"message": "Inscrição não encontrada"}), 404
