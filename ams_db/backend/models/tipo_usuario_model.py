from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.config.database import Base

class TipoUsuario(Base):
    __tablename__ = 'tipo_usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), unique=True, nullable=False)

    # 🔁 Relacionamento com Usuario
    usuarios = relationship("Usuario", back_populates="tipo_usuario", cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return f"<TipoUsuario(id={self.id}, nome='{self.nome}')>"
