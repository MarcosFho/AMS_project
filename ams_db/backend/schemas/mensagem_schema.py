from pydantic import BaseModel
from datetime import datetime

class MensagemCreateSchema(BaseModel):
    id_destinatario: int
    conteudo: str

class MensagemResponseSchema(MensagemCreateSchema):
    id: int
    id_remetente: int
    data_envio: datetime

    class Config:
        from_attributes = True  # ✅ Necessário para aceitar objetos ORM
