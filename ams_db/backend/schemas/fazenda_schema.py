from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List

class FazendaCreateSchema(BaseModel):
    nome: str
    telefone: Optional[str] = None
    id_endereco: Optional[int] = None
    descricao: Optional[str] = None
    area_total: Optional[float] = None



class FazendaFotoResponseSchema(BaseModel):
    id: int
    url_foto: str

    class Config:
        from_attributes = True

class FazendaResponseSchema(BaseModel):
    id: int
    id_usuario: int
    nome: str
    telefone: Optional[str] = None
    id_endereco: Optional[int] = None
    descricao: Optional[str] = None
    area_total: Optional[float] = None
    tipo_atividade: Optional[str] = None
    localizacao: Optional[str] = None
    data_criacao: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
    fotos: List[FazendaFotoResponseSchema] = []
    
    class Config:
        from_attributes = True  # Permite conversão ORM para Pydantic
 # Permite conversão ORM para Pydantic

class FazendaUpdateSchema(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    id_endereco: Optional[int] = None
    descricao: Optional[str] = None
    area_total: Optional[float] = None
    localizacao: Optional[str] = None
    tipo_atividade: Optional[str] = None
    fotos: List[FazendaFotoResponseSchema] = []
