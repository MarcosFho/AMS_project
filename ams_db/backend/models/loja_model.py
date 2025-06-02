from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.config.database import Base

class Loja(Base):
    __tablename__ = 'loja'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False, unique=True)
    nome = Column(String(100), nullable=False)
    cnpj = Column(String(18), nullable=False, unique=True)
    razao_social = Column(String(150))
    telefone = Column(String(20))
    id_endereco = Column(Integer, ForeignKey("endereco.id", ondelete="SET NULL"), nullable=True)

    data_criacao = Column(TIMESTAMP, server_default=func.now())
    data_atualizacao = Column(TIMESTAMP, onupdate=func.now())

    # 🔁 Relacionamentos
    usuario = relationship("Usuario", back_populates="loja")
    endereco = relationship("Endereco", back_populates="lojas", passive_deletes=True)

    def __repr__(self):
        return f"<Loja(id={self.id}, nome='{self.nome}', cnpj='{self.cnpj}')>"
