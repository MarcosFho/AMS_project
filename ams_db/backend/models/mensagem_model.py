from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.config.database import Base

class Mensagem(Base):
    __tablename__ = "mensagem"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_remetente = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    id_destinatario = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    conteudo = Column(Text, nullable=False)
    id_servico = Column(Integer, ForeignKey("servico.id"), nullable=True)   # NOVO
    id_fazenda = Column(Integer, ForeignKey("fazenda.id"), nullable=True)   # NOVO
    data_envio = Column(TIMESTAMP, server_default=func.current_timestamp())

    remetente = relationship("Usuario", foreign_keys=[id_remetente], back_populates="mensagens_enviadas", passive_deletes=True)
    destinatario = relationship("Usuario", foreign_keys=[id_destinatario], back_populates="mensagens_recebidas", passive_deletes=True)

    def __repr__(self):
        return f"<Mensagem(id={self.id}, de={self.id_remetente}, para={self.id_destinatario}, servico={self.id_servico}, fazenda={self.id_fazenda})>"
