from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 🔹 Schema para criação
class ClienteCreateSchema(BaseModel):
    id_usuario: Optional [int] = None
    id_endereco: Optional[int] = None

# 🔹 Schema para resposta
class ClienteResponseSchema(BaseModel):
    id: int
    id_usuario: Optional[int] = None
    id_endereco: Optional[int] = None
    data_registro: datetime
    data_atualizacao: Optional[datetime] = None

    class Config:
        from_attributes = True  # ✅ precisa estar DENTRO da classe
