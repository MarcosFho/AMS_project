from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.config.database import Base

class Prestador(Base):
    __tablename__ = 'prestador'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False, unique=True)
    localizacao = Column(String(255))
    avaliacao_media = Column(DECIMAL(3, 2), default=0)
    categoria = Column(String(50))
    data_atualizacao = Column(TIMESTAMP, onupdate=func.now())

    # 🔁 Relacionamento com Usuario
    usuario = relationship("Usuario", back_populates="prestador")


    def __repr__(self):
        return (
            f"<Prestador(id={self.id}, id_usuario={self.id_usuario}, "
            f"categoria='{self.categoria}', avaliacao_media={self.avaliacao_media})>"
        )
