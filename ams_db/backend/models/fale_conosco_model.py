from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.config.database import Base

class FaleConosco(Base):
    __tablename__ = 'fale_conosco'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    assunto = Column(String(100))
    mensagem = Column(Text, nullable=False)
    data_envio = Column(TIMESTAMP, server_default=func.current_timestamp())

    # 🔁 Relacionamento com Usuario
    usuario = relationship("Usuario", back_populates="fale_conoscos", passive_deletes=True)

    def __repr__(self):
        return f"<FaleConosco(id={self.id}, id_usuario={self.id_usuario}, assunto='{self.assunto}')>"
