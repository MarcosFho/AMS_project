from pydantic import BaseModel
from typing import Optional

class ServicoFotoCreateSchema(BaseModel):
    url_foto: str
    descricao: Optional[str] = None

class ServicoFotoResponseSchema(ServicoFotoCreateSchema):
    id: int
    id_servico: int

    class Config:
        from_attributes = True  # ✅ necessário para funcionar com objetos do SQLAlchemy

class ServicoFotoUpdateSchema(BaseModel):
    url_foto: Optional[str] = None
    descricao: Optional[str] = None
