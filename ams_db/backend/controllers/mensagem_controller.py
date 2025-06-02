from flask import Blueprint, request, jsonify
from middlewares.auth_middleware import auth_required
from backend.schemas.mensagem_schema import MensagemCreateSchema, MensagemResponseSchema
from backend.services.mensagem_service import enviar_mensagem, listar_mensagens

mensagem_bp = Blueprint("mensagem", __name__)

# 🔹 Enviar uma nova mensagem
@mensagem_bp.route("/api/mensagens", methods=["POST"])
@auth_required
def post_mensagem():
    dados = MensagemCreateSchema(**request.json)
    remetente_id = int(request.usuario_id)
    nova = enviar_mensagem(remetente_id, dados.id_destinatario, dados.conteudo)
    return jsonify(MensagemResponseSchema.model_validate(nova).model_dump()), 201

# 🔹 Listar mensagens entre usuário autenticado e outro usuário
@mensagem_bp.route("/api/mensagens/<int:id_destinatario>", methods=["GET"])
@auth_required
def get_mensagens(id_destinatario):
    remetente_id = int(request.usuario_id)
    conversas = listar_mensagens(remetente_id, id_destinatario)
    return jsonify([
        MensagemResponseSchema.model_validate(msg).model_dump()
        for msg in conversas
    ])
