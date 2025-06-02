from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.config.database import Base

class Solicitacao(Base):
    __tablename__ = "solicitacao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id", ondelete="CASCADE"), nullable=False)
    id_servico = Column(Integer, ForeignKey("servico.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="pendente")  # pendente, aceito, recusado, concluído
    data_criacao = Column(TIMESTAMP, server_default=func.current_timestamp())

    # 🔁 Relacionamentos com cliente e serviço
    cliente = relationship("Cliente", backref="solicitacoes", passive_deletes=True)
    servico = relationship("Servico", backref="solicitacoes", passive_deletes=True)

    def __repr__(self):
        return (
            f"<Solicitacao(id={self.id}, cliente={self.id_cliente}, "
            f"servico={self.id_servico}, status='{self.status}')>"
        )
