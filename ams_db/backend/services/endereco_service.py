from backend.models.endereco_model import Endereco
from backend.config.session import get_db

# 🔹 Criar um novo endereço
def criar_endereco(dados_endereco):
    with get_db() as db:
        endereco = Endereco(**dados_endereco)
        db.add(endereco)
        db.commit()              # ✅ salva no banco
        db.refresh(endereco)
        return endereco

# 🔹 Buscar endereço pelo ID
def buscar_endereco(id):
    with get_db() as db:
        return db.query(Endereco).filter(Endereco.id == id).first()

# 🔹 Atualizar endereço pelo ID
def atualizar_endereco(id, dados_endereco):
    with get_db() as db:
        endereco = db.query(Endereco).filter(Endereco.id == id).first()
        if endereco:
            for key, value in dados_endereco.items():
                setattr(endereco, key, value)
            db.commit()          # ✅ confirma a atualização
            db.refresh(endereco)
        return endereco

# 🔹 Excluir endereço pelo ID
def deletar_endereco(id):
    with get_db() as db:
        endereco = db.query(Endereco).filter(Endereco.id == id).first()
        if endereco:
            db.delete(endereco)
            db.commit()          # ✅ confirma a exclusão
        return endereco
