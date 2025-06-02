from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from backend.config.database import Base

class TrabalheConosco(Base):
    __tablename__ = 'trabalhe_conosco'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=True)
    mensagem = Column(Text, nullable=False)
    curriculo_link = Column(String(255), nullable=True)  # URL para o currículo
    data_envio = Column(TIMESTAMP, server_default=func.current_timestamp())

    def __repr__(self):
        return (
            f"<TrabalheConosco(id={self.id}, nome='{self.nome}', email='{self.email}')>"
        )
