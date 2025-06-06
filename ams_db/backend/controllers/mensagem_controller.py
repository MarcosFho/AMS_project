from flask import Blueprint, request, jsonify
from middlewares.auth_middleware import auth_required
from backend.schemas.mensagem_schema import MensagemCreateSchema, MensagemResponseSchema
from backend.services.mensagem_service import enviar_mensagem, listar_mensagens
from backend.config.session import get_db
from backend.models.mensagem_model import Mensagem
from backend.models.usuario_model import Usuario
from sqlalchemy import or_, desc

mensagem_bp = Blueprint("mensagem", __name__)

# 🔹 Enviar uma nova mensagem
@mensagem_bp.route("/mensagens", methods=["POST"])
@auth_required
def post_mensagem():
    dados = MensagemCreateSchema(**request.json)
    remetente_id = int(request.usuario_id)
    nova = enviar_mensagem(
        remetente_id, 
        dados.id_destinatario, 
        dados.conteudo, 
        id_servico=dados.id_servico, 
        id_fazenda=dados.id_fazenda
    )
    return jsonify(MensagemResponseSchema.model_validate(nova).model_dump()), 201


# 🔹 Listar mensagens entre usuário autenticado e outro usuário
@mensagem_bp.route("/mensagens/<int:id_destinatario>", methods=["GET"])
@auth_required
def get_mensagens(id_destinatario):
    remetente_id = int(request.usuario_id)
    conversas = listar_mensagens(remetente_id, id_destinatario)
    return jsonify([
        MensagemResponseSchema.model_validate(msg).model_dump()
        for msg in conversas
    ])

@mensagem_bp.route("/mensagens/servico/<int:id_servico>", methods=["GET"])
@auth_required
def get_mensagens_servico(id_servico):
    usuario_id = int(request.usuario_id)
    # listar todas mensagens desse serviço (pode filtrar por remetente/destinatário se quiser)
    with get_db() as db:
        msgs = db.query(Mensagem).filter(Mensagem.id_servico == id_servico).order_by(Mensagem.data_envio.asc()).all()
        return jsonify([MensagemResponseSchema.model_validate(msg).model_dump() for msg in msgs])
    

@mensagem_bp.route("/mensagens/fazenda/<int:id_fazenda>", methods=["GET"])
@auth_required
def get_mensagens_fazenda(id_fazenda):
    usuario_id = int(request.usuario_id)
    with get_db() as db:
        msgs = db.query(Mensagem).filter(Mensagem.id_fazenda == id_fazenda).order_by(Mensagem.data_envio.asc()).all()
        return jsonify([MensagemResponseSchema.model_validate(msg).model_dump() for msg in msgs])


# 🔹 Listar conversas do usuário autenticado
@mensagem_bp.route("/conversas", methods=["GET"])
@auth_required
def get_conversas():
    usuario_id = int(request.usuario_id)

    with get_db() as db:
        # Busca todos os IDs de usuários com quem já trocou mensagens
        ids_conversou = db.query(
            Mensagem.id_remetente
        ).filter(Mensagem.id_destinatario == usuario_id).union(
            db.query(Mensagem.id_destinatario).filter(Mensagem.id_remetente == usuario_id)
        ).distinct().all()

        ids_conversou = set([i[0] for i in ids_conversou if i[0] != usuario_id])
        conversas = []

        for outro_id in ids_conversou:
            # Busca a última mensagem entre o usuário logado e esse outro usuário
            ultima_msg = db.query(Mensagem).filter(
                or_(
                    (Mensagem.id_remetente == usuario_id) & (Mensagem.id_destinatario == outro_id),
                    (Mensagem.id_remetente == outro_id) & (Mensagem.id_destinatario == usuario_id),
                )
            ).order_by(desc(Mensagem.data_envio)).first()
            
            outro_usuario = db.query(Usuario).filter(Usuario.id == outro_id).first()

            # Só adiciona se existe pelo menos uma mensagem trocada
            if outro_usuario and ultima_msg:
                conversas.append({
                    "id": ultima_msg.id,
                    "outro_usuario": {
                        "id": outro_usuario.id,
                        "nome": outro_usuario.nome,
                        "telefone": outro_usuario.telefone,
                        "foto_url": outro_usuario.foto_url
                    },
                    "ultima_mensagem": ultima_msg.conteudo,
                    "data_ultima_mensagem": ultima_msg.data_envio.isoformat() if ultima_msg.data_envio else None
                })

        # Ordena por data da última mensagem (desc)
        conversas.sort(key=lambda x: x["data_ultima_mensagem"] or "", reverse=True)
        return jsonify(conversas)
