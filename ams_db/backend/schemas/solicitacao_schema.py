from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SolicitacaoCreateSchema(BaseModel):
    id_servico: int  # o cliente escolhe qual serviço quer solicitar

class SolicitacaoResponseSchema(BaseModel):
    id: int
    id_cliente: int
    id_servico: int
    status: str
    data_criacao: datetime

    class Config:
        from_attributes = True  # ✅ necessário para funcionar com objetos ORM
