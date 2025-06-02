from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.config.database import Base

class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True, autoincrement=True)

    id_usuario = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False, unique=True)
    id_endereco = Column(Integer, ForeignKey("endereco.id", ondelete="SET NULL"), nullable=True)

    data_registro = Column(TIMESTAMP, server_default=func.current_timestamp())
    data_atualizacao = Column(TIMESTAMP, onupdate=func.now())

    # ✅ Relacionamentos explícitos
    usuario = relationship("Usuario", back_populates="cliente", passive_deletes=True)
    endereco = relationship("Endereco", back_populates="clientes", passive_deletes=True)
    avaliacoes = relationship("Avaliacao", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self):
        return (
            f"<Cliente(id={self.id}, id_usuario={self.id_usuario}, "
            f"id_endereco={self.id_endereco}, data_registro={self.data_registro})>"
        )
