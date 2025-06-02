from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProdutoCreateSchema(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    desconto: Optional[float] = 0
    quantidade_estoque: Optional[int] = 0
    id_loja: int  # loja vinculada

class ProdutoResponseSchema(ProdutoCreateSchema):
    id: int
    data_criacao: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProdutoUpdateSchema(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    desconto: Optional[float] = None
    quantidade_estoque: Optional[int] = None
