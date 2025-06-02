# 🔹 Serviço para gerenciar fotos de produtos
from backend.config.session import get_db
from backend.models.produto_foto_model import ProdutoFoto

# 🔹 Criar uma nova foto de produto
def criar_produto_foto(dados_foto):
    with get_db() as db:
        foto = ProdutoFoto(**dados_foto)
        db.add(foto)
        db.commit()              # ✅ grava a foto
        db.refresh(foto)
        return foto

# 🔹 Listar todas as fotos de produto
def listar_fotos_produto():
    with get_db() as db:
        return db.query(ProdutoFoto).all()

# 🔹 Buscar foto de produto pelo ID
def buscar_produto_foto(id):
    with get_db() as db:
        return db.query(ProdutoFoto).filter(ProdutoFoto.id == id).first()

# 🔹 Atualizar uma foto de produto pelo ID
def atualizar_produto_foto(id, dados_foto):
    with get_db() as db:
        foto = db.query(ProdutoFoto).filter(ProdutoFoto.id == id).first()
        if foto:
            for key, value in dados_foto.items():
                setattr(foto, key, value)
            db.commit()          # ✅ salva atualização
            db.refresh(foto)
        return foto

# 🔹 Excluir uma foto de produto pelo ID
def deletar_foto_produto(id):
    with get_db() as db:
        foto = db.query(ProdutoFoto).filter(ProdutoFoto.id == id).first()
        if foto:
            db.delete(foto)
            db.commit()          # ✅ confirma exclusão
        return foto
# 🔹 Serviço para gerenciar fotos de produtos
from backend.config.session import get_db
from backend.models.produto_foto_model import ProdutoFoto

# 🔹 Criar uma nova foto de produto
def criar_produto_foto(dados_foto):
    with get_db() as db:
        foto = ProdutoFoto(**dados_foto)
        db.add(foto)
        db.commit()              # ✅ grava a foto
        db.refresh(foto)
        return foto

# 🔹 Listar todas as fotos de produto
def listar_fotos_produto():
    with get_db() as db:
        return db.query(ProdutoFoto).all()

# 🔹 Buscar foto de produto pelo ID
def buscar_produto_foto(id):
    with get_db() as db:
        return db.query(ProdutoFoto).filter(ProdutoFoto.id == id).first()

# 🔹 Atualizar uma foto de produto pelo ID
def atualizar_produto_foto(id, dados_foto):
    with get_db() as db:
        foto = db.query(ProdutoFoto).filter(ProdutoFoto.id == id).first()
        if foto:
            for key, value in dados_foto.items():
                setattr(foto, key, value)
            db.commit()          # ✅ salva atualização
            db.refresh(foto)
        return foto

# 🔹 Excluir uma foto de produto pelo ID
def deletar_produto_foto(id):
    with get_db() as db:
        foto = db.query(ProdutoFoto).filter(ProdutoFoto.id == id).first()
        if foto:
            db.delete(foto)
            db.commit()          # ✅ confirma exclusão
        return foto
