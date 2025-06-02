from backend.models.fazenda_foto_model import FazendaFoto
from backend.config.session import get_db

# 🔹 Adicionar uma foto de fazenda
def criar_fazenda_foto(dados_foto):
    with get_db() as db:
        foto = FazendaFoto(**dados_foto)
        db.add(foto)
        db.commit()              # ✅ salva a nova foto
        db.refresh(foto)
        return foto

# 🔹 Listar fotos de uma fazenda
def listar_fotos_fazenda(id_fazenda):
    with get_db() as db:
        return db.query(FazendaFoto).filter(FazendaFoto.id_fazenda == id_fazenda).all()
    
def atualizar_fazenda_foto(id, dados_foto):
    with get_db() as db:
        foto = db.query(FazendaFoto).filter(FazendaFoto.id == id).first()
        if foto:
            for key, value in dados_foto.items():
                setattr(foto, key, value)
            db.flush()
            db.refresh(foto)
            db.commit()
        return foto

# 🔹 Excluir foto de fazenda
def deletar_foto_fazenda(id):
    with get_db() as db:
        foto = db.query(FazendaFoto).filter(FazendaFoto.id == id).first()
        if foto:
            db.delete(foto)
            db.commit()          # ✅ confirma a exclusão
        return foto
