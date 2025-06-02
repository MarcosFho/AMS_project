from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class PrestadorCreateSchema(BaseModel):
    id_usuario: Optional[int] = None
    localizacao: Optional[str] = None
    avaliacao_media: Optional[float] = 0
    categoria: Optional[str] = None

class PrestadorResponseSchema(PrestadorCreateSchema):
    id: int
    data_atualizacao: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)  # ✅ compatível com Pydantic v2

# 🔄 Para atualizações parciais (exceto id_usuario)
class PrestadorUpdateSchema(BaseModel):
    localizacao: Optional[str] = None
    avaliacao_media: Optional[float] = None
    categoria: Optional[str] = None
