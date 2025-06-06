from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MensagemCreateSchema(BaseModel):
    id_destinatario: int
    conteudo: str
    id_servico: Optional[int] = None
    id_fazenda: Optional[int] = None

class MensagemResponseSchema(MensagemCreateSchema):
    id: int
    id_remetente: int
    data_envio: datetime

    class Config:
        from_attributes = True
