from pydantic import BaseModel
from typing import Optional
from datetime import date

# 🔹 Schema de criação (sem id_usuario, vem do token)
class PessoaFisicaCreateSchema(BaseModel):
    id_usuario: int  # ← agora validado pela Pydantic
    cpf: str
    rg: Optional[str] = None
    data_nascimento: Optional[date] = None

# 🔹 Schema de resposta
class PessoaFisicaResponseSchema(PessoaFisicaCreateSchema):
    id_usuario: int  # ← presente apenas na resposta

    class Config:
        from_attributes = True

# 🔹 Schema de atualização parcial (exceto ID e FK)
class PessoaFisicaUpdateSchema(BaseModel):
    cpf: Optional[str] = None
    rg: Optional[str] = None
    data_nascimento: Optional[date] = None
