from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.config.database import Base

class ProdutoFoto(Base):
    __tablename__ = 'produto_foto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_produto = Column(Integer, ForeignKey("produto.id", ondelete="CASCADE"), nullable=False)
    url_foto = Column(String(255), nullable=False)
    descricao = Column(String(100))

    # 🔁 Relacionamento com Produto
    produto = relationship("Produto", back_populates="fotos")

    def __repr__(self):
        return f"<ProdutoFoto(id={self.id}, id_produto={self.id_produto}, url_foto='{self.url_foto}')>"
