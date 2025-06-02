from backend.models.fale_conosco_model import FaleConosco
from backend.config.session import get_db

# 🔹 Criar uma nova mensagem de Fale Conosco
def criar_fale_conosco(dados_mensagem):
    with get_db() as db:
        mensagem = FaleConosco(**dados_mensagem)
        db.add(mensagem)
        db.commit()              # ✅ grava a mensagem
        db.refresh(mensagem)
        return mensagem

# 🔹 Listar todas as mensagens
def listar_fale_conosco():
    with get_db() as db:
        return db.query(FaleConosco).all()

# 🔹 Buscar mensagem por ID
def buscar_fale_conosco(id):
    with get_db() as db:
        return db.query(FaleConosco).filter(FaleConosco.id == id).first()

# 🔹 Excluir mensagem por ID
def deletar_fale_conosco(id):
    with get_db() as db:
        mensagem = db.query(FaleConosco).filter(FaleConosco.id == id).first()
        if mensagem:
            db.delete(mensagem)
            db.commit()          # ✅ confirma a exclusão
        return mensagem
