import os
import uuid
from werkzeug.utils import secure_filename
from sqlalchemy.orm import joinedload
from backend.models.fazenda_model import Fazenda
from backend.models.fazenda_foto_model import FazendaFoto
from backend.config.session import get_db

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../static/uploads/fazenda_fotos"))

def criar_fazenda(dados_fazenda, fotos=None):
    with get_db() as db:
        fazenda = Fazenda(**dados_fazenda)
        db.add(fazenda)
        db.commit()
        db.refresh(fazenda)
        fazenda_id = fazenda.id

        if fotos:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            for foto in fotos:
                if not foto or not foto.filename:
                    continue
                filename = f"{uuid.uuid4().hex}_{secure_filename(foto.filename)}"
                path_arquivo = os.path.join(UPLOAD_FOLDER, filename)
                foto.save(path_arquivo)
                url_foto = f"/uploads/fazenda_fotos/{filename}"
                foto_db = FazendaFoto(id_fazenda=fazenda_id, url_foto=url_foto)
                db.add(foto_db)
            db.commit()
        return fazenda_id

def listar_fazendas():
    with get_db() as db:
        return db.query(Fazenda).options(joinedload(Fazenda.fotos)).all()

def buscar_fazenda(id):
    with get_db() as db:
        return db.query(Fazenda).options(joinedload(Fazenda.fotos)).filter(Fazenda.id == id).first()

def atualizar_fazenda(id, dados_fazenda, fotos=None):
    with get_db() as db:
        fazenda = db.query(Fazenda).filter(Fazenda.id == id).first()
        if fazenda:
            for key, value in dados_fazenda.items():
                setattr(fazenda, key, value)
            # Atualiza fotos apenas se vierem novas
            if fotos:
                # Remove fotos antigas
                db.query(FazendaFoto).filter(FazendaFoto.id_fazenda == fazenda.id).delete()
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                for foto in fotos:
                    if not foto or not foto.filename:
                        continue
                    filename = f"{uuid.uuid4().hex}_{secure_filename(foto.filename)}"
                    path_arquivo = os.path.join(UPLOAD_FOLDER, filename)
                    foto.save(path_arquivo)
                    url_foto = f"/uploads/fazenda_fotos/{filename}"
                    foto_db = FazendaFoto(id_fazenda=fazenda.id, url_foto=url_foto)
                    db.add(foto_db)
            db.commit()
            db.refresh(fazenda)
            return fazenda.id
        return None

def deletar_fazenda(id):
    with get_db() as db:
        fazenda = db.query(Fazenda).filter(Fazenda.id == id).first()
        if fazenda:
            db.delete(fazenda)
            db.commit()
            return True
        return False
