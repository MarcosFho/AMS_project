from backend.models.fazenda_model import Fazenda
from backend.models.fazenda_foto_model import FazendaFoto

# 🔹 Criar uma nova fazenda
def criar_fazenda(dados_fazenda, db):
    fazenda = Fazenda(**dados_fazenda)
    db.add(fazenda)
    db.commit()
    db.refresh(fazenda)
    return fazenda

# 🔹 Listar todas as fazendas
def listar_fazendas(db):
    return db.query(Fazenda).all()

# 🔹 Buscar fazenda pelo ID
def buscar_fazenda(id, db):
    return db.query(Fazenda).filter(Fazenda.id == id).first()

# 🔹 Atualizar uma fazenda pelo ID
def atualizar_fazenda(id, dados_fazenda, db):
    fazenda = db.query(Fazenda).filter(Fazenda.id == id).first()
    if fazenda:
        for key, value in dados_fazenda.items():
            setattr(fazenda, key, value)
        db.commit()
        db.refresh(fazenda)
    return fazenda

# 🔹 Excluir uma fazenda pelo ID
def deletar_fazenda(id, db):
    fazenda = db.query(Fazenda).filter(Fazenda.id == id).first()
    if fazenda:
        db.delete(fazenda)
        db.commit()
    return fazenda

# 🔹 Listar fazendas com filtros opcionais (se desejar aplicar no futuro)
def listar_fazendas_filtradas(db, tipo_atividade=None, localizacao=None):
    query = db.query(Fazenda)

    if tipo_atividade:
        query = query.filter(Fazenda.tipo_atividade.ilike(f"%{tipo_atividade}%"))

    if localizacao:
        query = query.filter(Fazenda.localizacao.ilike(f"%{localizacao}%"))

    return query.all()
