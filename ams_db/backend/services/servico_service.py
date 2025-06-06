from backend.models.servico_model import Servico
from backend.config.session import get_db

# 🔹 Criar um novo serviço
def criar_servico(dados_servico, db):
    servico = Servico(**dados_servico)
    db.add(servico)
    db.commit()
    db.refresh(servico)
    return servico

# 🔹 Listar todos os serviços
def listar_servicos(db):
    return db.query(Servico).all()

# 🔹 Buscar serviço pelo ID
def buscar_servico(id_servico: int, db):
    return db.query(Servico).filter(Servico.id == id_servico).first()

# 🔹 Atualizar um serviço pelo ID
def atualizar_servico(id, dados_servico, db):
    servico = db.query(Servico).filter(Servico.id == id).first()
    if servico:
        for key, value in dados_servico.items():
            setattr(servico, key, value)
        db.commit()
        db.refresh(servico)
    return servico

# 🔹 Excluir um serviço pelo ID
def deletar_servico(id, db):
    servico = db.query(Servico).filter(Servico.id == id).first()
    if servico:
        db.delete(servico)
        db.commit()
    return servico

# 🔹 Listar serviços com filtros opcionais
def listar_servicos_filtrados(db, categoria=None, localizacao=None):
    query = db.query(Servico)

    if categoria:
        query = query.filter(Servico.categoria.ilike(f"%{categoria}%"))

    if localizacao:
        query = query.filter(Servico.localizacao.ilike(f"%{localizacao}%"))

    return query.all()
