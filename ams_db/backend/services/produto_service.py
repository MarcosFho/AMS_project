from backend.models.produto_model import Produto
from backend.config.session import get_db

def criar_produto(dados_produto):
    with get_db() as db:
        produto = Produto(**dados_produto)
        db.add(produto)
        db.commit()
        db.refresh(produto)
        return produto

def listar_produtos():
    with get_db() as db:
        return db.query(Produto).all()

def buscar_produto(id):
    with get_db() as db:
        return db.query(Produto).filter(Produto.id == id).first()

def atualizar_produto(id, dados_produto):
    with get_db() as db:
        produto = db.query(Produto).filter(Produto.id == id).first()
        if produto:
            for key, value in dados_produto.items():
                setattr(produto, key, value)
            db.commit()
            db.refresh(produto)
        return produto

def deletar_produto(id):
    with get_db() as db:
        produto = db.query(Produto).filter(Produto.id == id).first()
        if produto:
            db.delete(produto)
            db.commit()
        return produto
