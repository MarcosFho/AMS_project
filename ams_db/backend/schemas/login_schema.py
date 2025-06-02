from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# 🔹 Schema para criação de login
class LoginCreateSchema(BaseModel):
    id_usuario: int = Field(..., description="ID do usuário vinculado ao login")
    senha: str = Field(..., min_length=6, description="Senha em texto plano")

# 🔹 Resposta ao criar ou obter login
class LoginResponseSchema(BaseModel):
    id: int
    id_usuario: int
    ultimo_login: Optional[datetime]
    ativo: Optional[int]

    class Config:
        from_attributes = True  # ✅ necessário para uso com SQLAlchemy ORM (model_validate)

# 🔹 Schema para autenticação (login)
class LoginAuthSchema(BaseModel):
    email: EmailStr = Field(..., example="usuario@email.com")
    senha: str = Field(..., example="senha123")

# 🔹 Schema de retorno com token JWT
class TokenSchema(BaseModel):
    access_token: str = Field(..., description="Token de autenticação JWT")

# 🔹 Atualização parcial de login
class LoginUpdateSchema(BaseModel):
    senha: Optional[str] = Field(None, min_length=6, description="Nova senha em texto plano")
    ativo: Optional[int] = Field(None, description="Ativo = 1, Inativo = 0")
