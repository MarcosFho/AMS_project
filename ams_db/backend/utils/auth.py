import bcrypt
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
import os

# 🔐 Chave secreta segura
SECRET_KEY = os.getenv("SECRET_KEY", "chave_super_secreta_ams")
ALGORITHM = "HS256"
TOKEN_EXPIRATION_MINUTES = 60

# ✅ Gera hash seguro da senha
def gerar_hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# ✅ Compara senha enviada com hash salvo
def verificar_senha(senha: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))

# ✅ Cria token JWT com tempo de expiração
def gerar_token_jwt(dados: dict, exp_minutes: int = TOKEN_EXPIRATION_MINUTES) -> str:
    dados_copia = dados.copy()
    exp = datetime.utcnow() + timedelta(minutes=exp_minutes)
    dados_copia.update({"exp": exp})
    token = encode(dados_copia, SECRET_KEY, algorithm=ALGORITHM)
    return token

# ✅ Valida token JWT recebido
def verificar_token_jwt(token: str) -> dict:
    try:
        return decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise ValueError("Token expirado")
    except InvalidTokenError:
        raise ValueError("Token inválido")

