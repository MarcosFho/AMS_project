from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FaleConoscoCreateSchema(BaseModel):
    assunto: Optional[str]
    mensagem: str

class FaleConoscoResponseSchema(FaleConoscoCreateSchema):
    id: int
    data_envio: datetime  # ✅ Corrigido para datetime

    class Config:
        from_attributes = True  # ✅ Obrigatório com objetos ORM
