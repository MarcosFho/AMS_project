from flask import Blueprint, request, jsonify
from backend.schemas.avaliacao_schema import AvaliacaoCreateSchema, AvaliacaoResponseSchema
from backend.services.avaliacao_service import (
    criar_avaliacao, listar_avaliacoes, buscar_avaliacao,
    deletar_avaliacao
)
from backend.services.cliente_service import buscar_cliente_por_usuario
from backend.middlewares.auth_middleware import auth_required

avaliacao_bp = Blueprint('avaliacao', __name__)

# 🔹 Criar uma nova avaliação
@avaliacao_bp.route("/avaliacoes", methods=["POST"])
@auth_required
def post_avaliacao():
    usuario_id = int(request.usuario_id)

    cliente = buscar_cliente_por_usuario(usuario_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado para este usuário"}), 404

    dados = AvaliacaoCreateSchema(**request.json)
    avaliacao = criar_avaliacao(id_cliente=cliente.id, dados=dados)

    resposta = AvaliacaoResponseSchema.model_validate(avaliacao).model_dump()
    return jsonify(resposta), 201

# 🔹 Listar todas as avaliações
@avaliacao_bp.route("/avaliacoes", methods=["GET"])
def get_avaliacoes():
    avaliacoes = listar_avaliacoes()
    return jsonify([
        AvaliacaoResponseSchema.model_validate(a).model_dump()
        for a in avaliacoes
    ])

# 🔹 Buscar avaliação por ID
@avaliacao_bp.route("/avaliacoes/<int:id>", methods=["GET"])
def get_avaliacao(id):
    avaliacao = buscar_avaliacao(id)
    if avaliacao:
        resposta = AvaliacaoResponseSchema.model_validate(avaliacao).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Avaliação não encontrada"}), 404

# 🔹 Excluir avaliação por ID
@avaliacao_bp.route("/avaliacoes/<int:id>", methods=["DELETE"])
@auth_required
def delete_avaliacao(id):
    avaliacao = deletar_avaliacao(id)
    if avaliacao:
        return jsonify({"message": "Avaliação excluída com sucesso"})
    return jsonify({"message": "Avaliação não encontrada"}), 404
