from flask import Blueprint, request, jsonify
from middlewares.auth_middleware import auth_required
from backend.schemas.solicitacao_schema import SolicitacaoCreateSchema, SolicitacaoResponseSchema
from backend.services.solicitacao_service import (
    criar_solicitacao,
    listar_solicitacoes_por_cliente,
    atualizar_status_solicitacao
)
from backend.services.cliente_service import buscar_cliente_por_usuario
from backend.config.session import get_db
from backend.models.solicitacao_model import Solicitacao


solicitacao_bp = Blueprint('solicitacao', __name__)

# 🔹 Criar uma nova solicitação
@solicitacao_bp.route("/solicitacoes", methods=["POST"])
@auth_required
def post_solicitacao():
    usuario_id = int(request.usuario_id)

    # 🔍 Buscar o cliente correspondente ao usuário logado
    cliente = buscar_cliente_por_usuario(usuario_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado para este usuário"}), 404

    dados = SolicitacaoCreateSchema(**request.json)
    solicitacao = criar_solicitacao(id_cliente=cliente.id, id_servico=dados.id_servico)

    resposta = SolicitacaoResponseSchema.model_validate(solicitacao).model_dump()
    return jsonify(resposta), 201

# 🔹 Listar todas as solicitações do cliente autenticado
@solicitacao_bp.route("/solicitacoes", methods=["GET"])
@auth_required
def get_solicitacoes_cliente():
    usuario_id = int(request.usuario_id)
    cliente = buscar_cliente_por_usuario(usuario_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    solicitacoes = listar_solicitacoes_por_cliente(cliente.id)
    return jsonify([
        SolicitacaoResponseSchema.model_validate(s).model_dump()
        for s in solicitacoes
    ])

# 🔹 Atualizar status de uma solicitação
@solicitacao_bp.route("/solicitacoes/<int:id>/status", methods=["PUT"])
@auth_required
def put_status_solicitacao(id):
    dados = request.json
    novo_status = dados.get("status")
    if not novo_status:
        return jsonify({"message": "Campo 'status' é obrigatório"}), 400

    solicitacao = atualizar_status_solicitacao(id, novo_status)
    if solicitacao:
        return jsonify({"message": f"Status atualizado para '{novo_status}'"}), 200
    return jsonify({"message": "Solicitação não encontrada"}), 404

# 🔹 Deletar solicitação por ID
@solicitacao_bp.route("/solicitacoes/<int:id>", methods=["DELETE"])
@auth_required
def delete_solicitacao(id):

    with get_db() as db:
        solicitacao = db.query(Solicitacao).filter(Solicitacao.id == id).first()
        if not solicitacao:
            return jsonify({"message": "Solicitação não encontrada"}), 404

        db.delete(solicitacao)
        db.commit()
        return jsonify({"message": "Solicitação excluída com sucesso"}), 200