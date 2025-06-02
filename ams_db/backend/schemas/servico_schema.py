from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# 🔹 Schema para fotos (resposta)
class ServicoFotoSchema(BaseModel):
    id: int
    url_foto: str
    descricao: Optional[str] = None

    class Config:
        from_attributes = True

# 🔹 Schema para criação de serviço
class ServicoCreateSchema(BaseModel):
    tipo: str
    descricao: str
    preco: Optional[float] = None
    categoria: Optional[str] = None
    localizacao: Optional[str] = None

# 🔹 Schema para resposta de serviço
class ServicoResponseSchema(BaseModel):
    id: int
    tipo: str
    descricao: str
    preco: Optional[float] = None
    id_usuario: int
    categoria: Optional[str] = None
    localizacao: Optional[str] = None
    data_criacao: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
    fotos: List[ServicoFotoSchema] = []  # ← agora aceita objetos de foto

    class Config:
        from_attributes = True

# 🔹 Schema para atualização de serviço
class ServicoUpdateSchema(BaseModel):
    tipo: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    categoria: Optional[str] = None
    localizacao: Optional[str] = None
