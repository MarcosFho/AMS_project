from backend.models.fazenda_model import Fazenda
from backend.config.session import get_db

# 🔹 Criar uma nova fazenda
def criar_fazenda(dados_fazenda):
    with get_db() as db:
        fazenda = Fazenda(**dados_fazenda)
        db.add(fazenda)
        db.commit()              # ✅ salva no banco
        db.refresh(fazenda)
        return fazenda

# 🔹 Listar todas as fazendas
def listar_fazendas():
    with get_db() as db:
        return db.query(Fazenda).all()

# 🔹 Buscar fazenda pelo ID
def buscar_fazenda(id):
    with get_db() as db:
        return db.query(Fazenda).filter(Fazenda.id == id).first()

# 🔹 Atualizar uma fazenda pelo ID
def atualizar_fazenda(id, dados_fazenda):
    with get_db() as db:
        fazenda = db.query(Fazenda).filter(Fazenda.id == id).first()
        if fazenda:
            for key, value in dados_fazenda.items():
                setattr(fazenda, key, value)
            db.commit()          # ✅ confirma a atualização
            db.refresh(fazenda)
        return fazenda

# 🔹 Excluir uma fazenda pelo ID
def deletar_fazenda(id):
    with get_db() as db:
        fazenda = db.query(Fazenda).filter(Fazenda.id == id).first()
        if fazenda:
            db.delete(fazenda)
            db.commit()          # ✅ confirma exclusão
        return fazenda
