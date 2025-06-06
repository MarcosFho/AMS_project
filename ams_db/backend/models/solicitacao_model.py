from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.config.database import Base

class Solicitacao(Base):
    __tablename__ = "solicitacao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    id_servico = Column(Integer, ForeignKey("servico.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="pendente")
    data_criacao = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relacionamentos usando back_populates
    usuario = relationship("Usuario", back_populates="solicitacoes")
    servico = relationship("Servico", back_populates="solicitacoes")

    def __repr__(self):
        return (
            f"<Solicitacao(id={self.id}, usuario={self.id_usuario}, "
            f"servico={self.id_servico}, status='{self.status}')>"
        )
