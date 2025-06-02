from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# 🔹 Esquema da Foto da Fazenda
class FazendaFotoSchema(BaseModel):
    id: int
    url_foto: str
    descricao: Optional[str] = None

    class Config:
        from_attributes = True

# 🔹 Criação de Fazenda
class FazendaCreateSchema(BaseModel):
    nome: str
    telefone: Optional[str] = None
    id_endereco: Optional[int] = None
    descricao: Optional[str] = None
    area_total: Optional[float] = None
    tipo_atividade: str
    localizacao: str
    id_usuario: int  # 🔒 necessário pois é FK obrigatória no banco

# 🔹 Atualização de Fazenda
class FazendaUpdateSchema(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    descricao: Optional[str] = None
    area_total: Optional[float] = None
    tipo_atividade: Optional[str] = None
    localizacao: Optional[str] = None
    

# 🔹 Resposta de Fazenda
class FazendaResponseSchema(BaseModel):
    id: int
    nome: str
    telefone: Optional[str] = None
    id_endereco: Optional[int] = None
    descricao: Optional[str] = None
    area_total: Optional[float] = None
    tipo_atividade: Optional[str] = None
    localizacao: Optional[str] = None
    data_criacao: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
    fotos: Optional[List[FazendaFotoSchema]] = []
    usuario_id: Optional[int] = None 

    class Config:
        from_attributes = True  # para Pydantic v2+
