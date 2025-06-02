from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.config.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    telefone = Column(String(20), nullable=True)
    foto_url = Column(String(255), nullable=True)

    # 🔹 Relacionamento com endereço
    id_endereco = Column(Integer, ForeignKey("endereco.id", ondelete="SET NULL"))
    endereco = relationship("Endereco", back_populates="usuarios")

    # 🔹 Tipo de usuário
    tipo_usuario_id = Column(Integer, ForeignKey("tipo_usuario.id"), nullable=False)
    tipo_usuario = relationship("TipoUsuario", back_populates="usuarios")

    status = Column(String(20), default="ATIVO")

    # 🔹 Relacionamentos com entidades associadas
    cliente = relationship("Cliente", back_populates="usuario", uselist=False)
    prestador = relationship("Prestador", back_populates="usuario", uselist=False)
    loja = relationship("Loja", back_populates="usuario", uselist=False)
    fale_conoscos = relationship("FaleConosco", back_populates="usuario", cascade="all, delete-orphan")

    # 🔹 Login 1:1 (se ainda for necessário incluir)
    login = relationship("Login", back_populates="usuario", uselist=False, cascade="all, delete-orphan")


    # 🔹 Auditoria
    data_criacao = Column(TIMESTAMP, server_default=func.now())
    data_atualizacao = Column(TIMESTAMP, onupdate=func.now())

    def __repr__(self):
        return f"<Usuario(id={self.id}, nome='{self.nome}')>"
