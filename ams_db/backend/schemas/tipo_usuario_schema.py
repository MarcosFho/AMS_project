from pydantic import BaseModel
from typing import Optional

class TipoUsuarioCreateSchema(BaseModel):
    nome: str

class TipoUsuarioResponseSchema(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True  # ✅ necessário para uso com SQLAlchemy ORM

class TipoUsuarioUpdateSchema(BaseModel):
    nome: Optional[str] = None  # ✅ permite atualização parcial
