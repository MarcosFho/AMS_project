from backend.models.tipo_usuario_model import TipoUsuario
from backend.config.session import get_db

# 🔹 Listar todos os tipos de usuário
def listar_tipos_usuario():
    with get_db() as db:
        return db.query(TipoUsuario).all()

# 🔹 Buscar tipo de usuário por ID
def buscar_tipo_usuario(id):
    with get_db() as db:
        return db.query(TipoUsuario).filter(TipoUsuario.id == id).first()

# 🔹 Criar novo tipo de usuário
def criar_tipo_usuario(dados):
    with get_db() as db:
        tipo = TipoUsuario(**dados)
        db.add(tipo)
        db.commit()              # ✅ grava no banco
        db.refresh(tipo)
        return tipo

# 🔹 Atualizar tipo de usuário
def atualizar_tipo_usuario(id, dados):
    with get_db() as db:
        tipo = db.query(TipoUsuario).filter(TipoUsuario.id == id).first()
        if tipo:
            for key, value in dados.items():
                setattr(tipo, key, value)
            db.commit()          # ✅ confirma atualização
            db.refresh(tipo)
        return tipo

# 🔹 Excluir tipo de usuário
def deletar_tipo_usuario(id):
    with get_db() as db:
        tipo = db.query(TipoUsuario).filter(TipoUsuario.id == id).first()
        if tipo:
            db.delete(tipo)
            db.commit()          # ✅ confirma exclusão
        return tipo
