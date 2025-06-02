from pydantic import BaseModel
from typing import Optional

class FazendaFotoCreateSchema(BaseModel):
    url_foto: str
    descricao: Optional[str] = None

class FazendaFotoResponseSchema(FazendaFotoCreateSchema):
    id: int
    id_fazenda: int

    class Config:
        from_attributes = True  # ✅ necessário para uso com ORM (SQLAlchemy)

# 🔹 Atualização sem campos de integridade
class FazendaFotoUpdateSchema(BaseModel):
    url_foto: Optional[str] = None
    descricao: Optional[str] = None
