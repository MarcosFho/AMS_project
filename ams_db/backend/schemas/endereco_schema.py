from pydantic import BaseModel
from typing import Optional

# 🔹 Schema de criação
class EnderecoCreateSchema(BaseModel):
    rua: str
    numero: str
    bairro: str
    cidade: str
    estado: str
    cep: str
    complemento: Optional[str] = None

# 🔹 Schema de resposta
class EnderecoResponseSchema(EnderecoCreateSchema):
    id: int

    class Config:
        from_attributes = True  # ✅ para uso com ORM

# 🔹 Novo schema de atualização parcial
class EnderecoUpdateSchema(BaseModel):
    rua: Optional[str] = None
    numero: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    complemento: Optional[str] = None
