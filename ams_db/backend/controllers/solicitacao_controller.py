from flask import Blueprint, request, jsonify
from middlewares.auth_middleware import auth_required
from backend.schemas.solicitacao_schema import SolicitacaoCreateSchema, SolicitacaoResponseSchema
from backend.services.solicitacao_service import (
    criar_solicitacao,
    listar_solicitacoes_por_usuario,
    atualizar_status_solicitacao
)
from backend.services.mensagem_service import enviar_mensagem
from backend.services.servico_service import buscar_servico 
from backend.config.session import get_db
from backend.models.solicitacao_model import Solicitacao

solicitacao_bp = Blueprint('solicitacao', __name__)

# 🔹 Criar uma nova solicitação
@solicitacao_bp.route("/solicitacoes", methods=["POST"])
@auth_required
def post_solicitacao():
    usuario_id = int(request.usuario_id)
    dados = SolicitacaoCreateSchema(**request.json)
    solicitacao = criar_solicitacao(id_usuario=usuario_id, id_servico=dados.id_servico)

    # Buscar serviço para enviar mensagem automática
    with get_db() as db:
        servico = buscar_servico(dados.id_servico, db)   # <--- passe o db aqui!
        if servico:
            id_remetente = usuario_id
            id_destinatario = servico.id_usuario
            conteudo = "Olá! Gostaria de conversar sobre o seu serviço."
            try:
                enviar_mensagem(id_remetente, id_destinatario, conteudo)
            except Exception as e:
                print("Erro ao enviar mensagem automática:", e)

    resposta = SolicitacaoResponseSchema.model_validate(solicitacao).model_dump()
    return jsonify(resposta), 201

# 🔹 Listar todas as solicitações do usuário autenticado
@solicitacao_bp.route("/solicitacoes", methods=["GET"])
@auth_required
def get_solicitacoes_usuario():
    usuario_id = int(request.usuario_id)
    solicitacoes = listar_solicitacoes_por_usuario(usuario_id)
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
