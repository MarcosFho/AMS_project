from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.config.database import Base

class Servico(Base):
    __tablename__ = 'servico'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(50), nullable=False)
    descricao = Column(Text, nullable=False)
    preco = Column(DECIMAL(10, 2))
    id_usuario = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    categoria = Column(String(50))
    localizacao = Column(String(255))
    data_criacao = Column(TIMESTAMP, server_default=func.now())
    data_atualizacao = Column(TIMESTAMP, onupdate=func.now())

    # 🔁 Relacionamento com Usuario
    usuario = relationship("Usuario", back_populates="servicos", passive_deletes=True)
    avaliacoes = relationship("Avaliacao", back_populates="servico", cascade="all, delete-orphan")
    solicitacoes = relationship("Solicitacao", back_populates="servico", passive_deletes=True)



    def __repr__(self):
        return f"<Servico(id={self.id}, tipo='{self.tipo}', preco={self.preco})>"
