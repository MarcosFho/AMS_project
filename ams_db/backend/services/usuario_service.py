from backend.config.session import get_db
from backend.models.usuario_model import Usuario

# 🔹 Criar um novo usuário
def criar_usuario(dados_usuario):
    with get_db() as db:
        usuario = Usuario(**dados_usuario)
        db.add(usuario)
        db.commit()              # ✅ grava no banco
        db.refresh(usuario)
        return usuario

# 🔹 Listar todos os usuários
def listar_usuarios():
    with get_db() as db:
        return db.query(Usuario).all()

# 🔹 Buscar um usuário pelo ID
def buscar_usuario(id):
    with get_db() as db:
        return db.query(Usuario).filter(Usuario.id == id).first()

# 🔹 Atualizar um usuário pelo ID
def atualizar_usuario(id, dados_usuario):
    with get_db() as db:
        usuario = db.query(Usuario).filter(Usuario.id == id).first()
        if usuario:
            for key, value in dados_usuario.items():
                setattr(usuario, key, value)
            db.commit()          # ✅ confirma atualização
            db.refresh(usuario)
        return usuario

# 🔹 Excluir um usuário pelo ID
def deletar_usuario(id):
    with get_db() as db:
        usuario = db.query(Usuario).filter(Usuario.id == id).first()
        if usuario:
            db.delete(usuario)
            db.commit()          # ✅ confirma exclusão
        return usuario
