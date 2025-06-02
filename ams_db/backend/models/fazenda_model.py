from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.config.database import Base

class Fazenda(Base):
    __tablename__ = 'fazenda'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20))
    id_endereco = Column(Integer, ForeignKey("endereco.id", ondelete="SET NULL"), nullable=True)
    descricao = Column(Text)
    area_total = Column(DECIMAL(10, 2))
    tipo_atividade = Column(String(100))
    localizacao = Column(String(150))
    data_criacao = Column(TIMESTAMP, server_default=func.now())
    data_atualizacao = Column(TIMESTAMP, onupdate=func.now())

    # Relacionamentos
    usuario = relationship("Usuario", backref="fazendas", passive_deletes=True)
    endereco = relationship("Endereco", back_populates="fazendas", passive_deletes=True)
    fotos = relationship("FazendaFoto", back_populates="fazenda", cascade="all, delete-orphan")

    def __repr__(self):
        return (
            f"<Fazenda(id={self.id}, nome='{self.nome}', area_total={self.area_total})>"
        )
