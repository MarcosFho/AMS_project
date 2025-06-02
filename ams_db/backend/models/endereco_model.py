from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.config.database import Base

class Endereco(Base):
    __tablename__ = 'endereco'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rua = Column(String(100), nullable=False)
    numero = Column(String(100), nullable=False)
    bairro = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(10), nullable=False)
    complemento = Column(String(100))

    # 🔁 Relacionamentos com nomes únicos para evitar conflitos
    usuarios = relationship("Usuario", back_populates="endereco", passive_deletes=True)
    clientes = relationship("Cliente", back_populates="endereco", passive_deletes=True)
    fazendas = relationship("Fazenda", back_populates="endereco", passive_deletes=True)
    lojas = relationship("Loja", back_populates="endereco", passive_deletes=True)

    def __repr__(self):
        return (
            f"<Endereco(id={self.id}, rua='{self.rua}', numero='{self.numero}', "
            f"bairro='{self.bairro}', cidade='{self.cidade}', estado='{self.estado}', cep='{self.cep}')>"
        )
