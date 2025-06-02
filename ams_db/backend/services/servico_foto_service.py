from backend.models.servico_foto_model import ServicoFoto
from backend.config.session import get_db

# 🔹 Criar nova foto de serviço
def criar_servico_foto(dados_foto):
    with get_db() as db:
        foto = ServicoFoto(**dados_foto)
        db.add(foto)
        db.commit()
        db.refresh(foto)
        return foto

# 🔹 Listar fotos de um serviço
def listar_fotos_servico(id_servico):
    with get_db() as db:
        return db.query(ServicoFoto).filter(ServicoFoto.id_servico == id_servico).all()

# 🔹 Buscar uma única foto de serviço por ID
def buscar_servico_foto(id_foto):
    with get_db() as db:
        return db.query(ServicoFoto).filter(ServicoFoto.id == id_foto).first()

# 🔹 Atualizar dados de uma foto de serviço (exceto id_servico)
def atualizar_servico_foto(id_foto, dados):
    with get_db() as db:
        foto = db.query(ServicoFoto).filter(ServicoFoto.id == id_foto).first()
        if foto:
            for key, value in dados.items():
                setattr(foto, key, value)
            db.commit()
            db.refresh(foto)
        return foto

# 🔹 Deletar uma foto de serviço
def deletar_foto_servico(id_foto):
    with get_db() as db:
        foto = db.query(ServicoFoto).filter(ServicoFoto.id == id_foto).first()
        if foto:
            db.delete(foto)
            db.commit()
        return foto
