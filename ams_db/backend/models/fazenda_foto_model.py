from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.config.database import Base

class FazendaFoto(Base):
    __tablename__ = 'fazenda_foto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_fazenda = Column(Integer, ForeignKey("fazenda.id", ondelete="CASCADE"), nullable=False)
    url_foto = Column(String(255), nullable=False)
    descricao = Column(String(100))

    # 🔁 Relacionamento com Fazenda
    fazenda = relationship("Fazenda", back_populates="fotos", passive_deletes=True)

    def __repr__(self):
        return f"<FazendaFoto(id={self.id}, id_fazenda={self.id_fazenda}, url_foto='{self.url_foto}')>"
