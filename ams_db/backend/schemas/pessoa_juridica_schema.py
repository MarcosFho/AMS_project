from pydantic import BaseModel
from typing import Optional

class PessoaJuridicaCreateSchema(BaseModel):
    id_usuario: int
    razao_social: str
    cnpj: str
    cnae: Optional[str] = None
    inscricao_estadual: Optional[str] = None

class PessoaJuridicaUpdateSchema(BaseModel):
    razao_social: Optional[str] = None
    cnpj: Optional[str] = None
    cnae: Optional[str] = None
    inscricao_estadual: Optional[str] = None

class PessoaJuridicaResponseSchema(PessoaJuridicaCreateSchema):
    class Config:
        from_attributes = True  # ✅ compatível com ORM
