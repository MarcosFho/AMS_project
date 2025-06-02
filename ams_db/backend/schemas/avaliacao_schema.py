from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AvaliacaoCreateSchema(BaseModel):
    id_servico: int
    nota: float = Field(..., ge=1.0, le=5.0)
    comentario: Optional[str] = None

class AvaliacaoResponseSchema(BaseModel):
    id: int
    id_servico: int
    id_cliente: int
    nota: float
    comentario: Optional[str] = None
    data_avaliacao: datetime

    class Config:
        from_attributes = True  # ✅ Necessário para .model_validate(objeto ORM)
