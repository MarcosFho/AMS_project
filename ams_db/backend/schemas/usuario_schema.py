from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from backend.schemas.endereco_schema import EnderecoResponseSchema
from typing import Optional



# 🔹 Schema de criação de usuário
class UsuarioCreateSchema(BaseModel):
    nome: str
    email: EmailStr
    telefone: str
    senha: str = Field(min_length=6)
    tipo_usuario: str  # PRESTADOR, CLIENTE, ADMIN, USUARIO
    endereco_id: Optional[int] = None
    foto_url: Optional[str] = None
    

# 🔹 Schema de resposta de usuário
class UsuarioResponseSchema(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str
    tipo_usuario_id: int
    endereco_id: Optional[int] = None
    endereco: Optional[EnderecoResponseSchema] = None   # <--- ADICIONE ISSO
    foto_url: Optional[str] = None
    data_criacao: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None

    class Config:
        from_attributes = True  # necessário para uso com SQLAlchemy

# 🔹 Schema para atualização (parcial)
class UsuarioUpdateSchema(BaseModel):
    nome: Optional[str]
    email: Optional[EmailStr]
    telefone: Optional[str]
    foto_url: Optional[str]
