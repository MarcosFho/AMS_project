from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.config.database import Base

class Produto(Base):
    __tablename__ = 'produto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    preco = Column(DECIMAL(10, 2), nullable=False)
    desconto = Column(DECIMAL(5, 2), default=0)
    quantidade_estoque = Column(Integer, default=0)
    id_loja = Column(Integer, ForeignKey("loja.id", ondelete="CASCADE"), nullable=False)

    data_criacao = Column(TIMESTAMP, server_default=func.now())
    data_atualizacao = Column(TIMESTAMP, onupdate=func.now())

    # 🔁 Relacionamentos
    loja = relationship("Loja", backref="produtos", passive_deletes=True)
    fotos = relationship("ProdutoFoto", back_populates="produto", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Produto(id={self.id}, nome='{self.nome}', preco={self.preco})>"
