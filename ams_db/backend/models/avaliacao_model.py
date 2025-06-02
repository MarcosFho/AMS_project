from sqlalchemy import Column, Integer, Text, Float, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.config.database import Base

class Avaliacao(Base):
    __tablename__ = 'avaliacao'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_servico = Column(Integer, ForeignKey("servico.id"), nullable=False)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    nota = Column(Float, nullable=False)
    comentario = Column(Text)
    data_avaliacao = Column(TIMESTAMP, server_default=func.current_timestamp())

    # 🔄 RELACIONAMENTOS
    servico = relationship("Servico", back_populates="avaliacoes")
    cliente = relationship("Cliente", back_populates="avaliacoes")

    def __repr__(self):
        return (
            f"<Avaliacao(id={self.id}, nota={self.nota}, "
            f"comentario='{self.comentario}', id_servico={self.id_servico}, id_cliente={self.id_cliente})>"
        )
