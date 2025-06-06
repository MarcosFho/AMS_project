from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SolicitacaoCreateSchema(BaseModel):
    id_servico: int  # o usuário escolhe qual serviço quer solicitar

class SolicitacaoResponseSchema(BaseModel):
    id: int
    id_usuario: int      # <-- corrigido para refletir o model novo!
    id_servico: int
    status: str
    data_criacao: datetime

    class Config:
        from_attributes = True  # ✅ necessário para funcionar com objetos ORM
