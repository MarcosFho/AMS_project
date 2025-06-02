from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TrabalheConoscoCreateSchema(BaseModel):
    nome: str
    email: str
    telefone: Optional[str] = None
    mensagem: str
    curriculo_link: Optional[str] = None

class TrabalheConoscoResponseSchema(TrabalheConoscoCreateSchema):
    id: int
    data_envio: datetime

    class Config:
        from_attributes = True  # ✅ Permite converter modelos SQLAlchemy diretamente
