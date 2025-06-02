from backend.models.login_model import Login
from backend.models.usuario_model import Usuario
from backend.utils.crypto import verificar_senha, gerar_hash_senha
from backend.config.session import get_db
from backend.utils.auth import gerar_token_jwt
from datetime import datetime

# 🔹 Criar novo login
def criar_login(dados, db=None):
    own_session = False
    if db is None:
        db = next(get_db())
        own_session = True

    login = Login(**dados)
    db.add(login)

    if own_session:
        db.commit()
        db.refresh(login)

    return login

# 🔹 Buscar login por ID de usuário
def buscar_login_por_usuario(id_usuario):
    with get_db() as db:
        return db.query(Login).filter(Login.id_usuario == id_usuario).first()

# 🔹 Atualizar login parcial (ex: redefinir senha, status, etc)
def atualizar_login(id_usuario, dados):
    with get_db() as db:
        login = db.query(Login).filter(Login.id_usuario == id_usuario).first()
        if login:
            if 'senha' in dados:
                dados['senha_hash'] = gerar_hash_senha(dados.pop('senha'))
            for key, value in dados.items():
                setattr(login, key, value)
            db.commit()
            db.refresh(login)
        return login

# 🔹 Atualizar último login
def atualizar_ultimo_login(id_usuario):
    with get_db() as db:
        login = db.query(Login).filter(Login.id_usuario == id_usuario).first()
        if login:
            login.ultimo_login = datetime.utcnow()
            db.commit()
        return login

# 🔹 Autenticar por email e senha e gerar token JWT
def autenticar_usuario(email: str, senha: str) -> str:
    with get_db() as db:
        usuario = db.query(Usuario).filter(Usuario.email == email).first()
        if not usuario:
            return None

        login = db.query(Login).filter(Login.id_usuario == usuario.id).first()
        if login and login.ativo == 1 and verificar_senha(senha, login.senha_hash):
            atualizar_ultimo_login(usuario.id)
            return gerar_token_jwt({"sub": str(usuario.id)})
        return None

# 🔹 Redefinir senha (com hash)
def redefinir_senha(id_usuario: int, nova_senha: str):
    with get_db() as db:
        login = db.query(Login).filter(Login.id_usuario == id_usuario).first()
        if login:
            login.senha_hash = gerar_hash_senha(nova_senha)
            db.commit()

# 🔹 Ativar conta de usuário
def ativar_usuario(id_usuario: int):
    with get_db() as db:
        login = db.query(Login).filter(Login.id_usuario == id_usuario).first()
        if login:
            login.ativo = 1
            db.commit()
