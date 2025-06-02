from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FazendaCreateSchema(BaseModel):
    nome: str
    telefone: Optional[str] = None
    id_endereco: Optional[int] = None
    descricao: Optional[str] = None
    area_total: Optional[float] = None

class FazendaResponseSchema(BaseModel):
    id: int
    nome: str
    telefone: Optional[str] = None
    id_endereco: Optional[int] = None
    descricao: Optional[str] = None
    area_total: Optional[float] = None
    data_criacao: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None

    class Config:
        from_attributes = True  # Permite conversão ORM para Pydantic

class FazendaUpdateSchema(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    id_endereco: Optional[int] = None
    descricao: Optional[str] = None
    area_total: Optional[float] = None
