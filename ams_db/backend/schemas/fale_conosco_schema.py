# backend/schemas/fale_conosco_schema.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FaleConoscoCreateSchema(BaseModel):
    assunto: Optional[str] = None
    mensagem: str = Field(..., min_length=1, description="A mensagem é obrigatória e não pode estar vazia")

class FaleConoscoResponseSchema(FaleConoscoCreateSchema):
    id: int
    id_usuario: int
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    data_envio: datetime

    class Config:
        from_attributes = True
