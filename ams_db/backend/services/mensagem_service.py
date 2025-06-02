from backend.models.mensagem_model import Mensagem
from backend.config.session import get_db

# 🔹 Enviar uma nova mensagem
def enviar_mensagem(id_remetente: int, id_destinatario: int, conteudo: str):
    with get_db() as db:
        nova = Mensagem(
            id_remetente=id_remetente,
            id_destinatario=id_destinatario,
            conteudo=conteudo
        )
        db.add(nova)
        db.commit()              # ✅ grava a mensagem
        db.refresh(nova)
        return nova

# 🔹 Listar mensagens entre dois usuários
def listar_mensagens(id_usuario1: int, id_usuario2: int):
    with get_db() as db:
        return db.query(Mensagem).filter(
            ((Mensagem.id_remetente == id_usuario1) & (Mensagem.id_destinatario == id_usuario2)) |
            ((Mensagem.id_remetente == id_usuario2) & (Mensagem.id_destinatario == id_usuario1))
        ).order_by(Mensagem.data_envio.asc()).all()
