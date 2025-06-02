from backend.models.trabalhe_conosco_model import TrabalheConosco
from backend.config.session import get_db

# 🔹 Criar um novo cadastro Trabalhe Conosco
def criar_trabalhe_conosco(dados_cadastro):
    with get_db() as db:
        cadastro = TrabalheConosco(**dados_cadastro)
        db.add(cadastro)
        db.commit()              # ✅ grava no banco
        db.refresh(cadastro)
        return cadastro

# 🔹 Listar todos os cadastros Trabalhe Conosco
def listar_trabalhe_conosco():
    with get_db() as db:
        return db.query(TrabalheConosco).all()

# 🔹 Buscar cadastro Trabalhe Conosco pelo ID
def buscar_trabalhe_conosco(id):
    with get_db() as db:
        return db.query(TrabalheConosco).filter(TrabalheConosco.id == id).first()

# 🔹 Excluir um cadastro Trabalhe Conosco pelo ID
def deletar_trabalhe_conosco(id):
    with get_db() as db:
        cadastro = db.query(TrabalheConosco).filter(TrabalheConosco.id == id).first()
        if cadastro:
            db.delete(cadastro)
            db.commit()          # ✅ confirma exclusão
        return cadastro
