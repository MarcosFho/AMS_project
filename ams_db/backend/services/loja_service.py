from backend.models.loja_model import Loja
from backend.config.session import get_db

def criar_loja(dados_loja):
    with get_db() as db:
        loja = Loja(**dados_loja)
        db.add(loja)
        db.commit()
        db.refresh(loja)
        return loja

def listar_lojas():
    with get_db() as db:
        return db.query(Loja).all()

def buscar_loja(id):
    with get_db() as db:
        return db.query(Loja).filter(Loja.id == id).first()

def atualizar_loja(id, dados_loja):
    with get_db() as db:
        loja = db.query(Loja).filter(Loja.id == id).first()
        if loja:
            for key, value in dados_loja.items():
                setattr(loja, key, value)
            db.commit()
            db.refresh(loja)
        return loja

def deletar_loja(id):
    with get_db() as db:
        loja = db.query(Loja).filter(Loja.id == id).first()
        if loja:
            db.delete(loja)
            db.commit()
        return loja
