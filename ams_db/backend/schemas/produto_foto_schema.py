from pydantic import BaseModel
from typing import Optional

class ProdutoFotoCreateSchema(BaseModel):
    url_foto: str
    descricao: Optional[str] = None

class ProdutoFotoResponseSchema(ProdutoFotoCreateSchema):
    id: int
    id_produto: int

    class Config:
        from_attributes = True  # ✅ necessário para aceitar objetos do SQLAlchemy

# ✅ Atualização parcial (sem permitir alteração de id ou id_produto)
class ProdutoFotoUpdateSchema(BaseModel):
    url_foto: Optional[str] = None
    descricao: Optional[str] = None
