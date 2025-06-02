from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LojaCreateSchema(BaseModel):
    nome: str
    cnpj: str
    razao_social: Optional[str] = None
    telefone: Optional[str] = None
    id_endereco: Optional[int] = None

class LojaResponseSchema(LojaCreateSchema):
    id: int
    data_criacao: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None

    class Config:
        from_attributes = True

class LojaUpdateSchema(BaseModel):
    nome: Optional[str] = None
    razao_social: Optional[str] = None
    telefone: Optional[str] = None
    id_endereco: Optional[int] = None
