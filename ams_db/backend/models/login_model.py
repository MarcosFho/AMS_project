from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.config.database import Base

class Login(Base):
    """
    Modelo de Login vinculado a um usuário.
    Armazena a hash da senha, status de ativação e data do último login.
    """
    __tablename__ = 'login'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable=False)

    # Salva a última vez que o usuário fez login
    ultimo_login = Column(TIMESTAMP, nullable=True)

    # Usuário ativo ou não
    ativo = Column(Boolean, default=True, nullable=False)

    # 🔁 Relacionamento bidirecional com Usuario
    usuario = relationship("Usuario", back_populates="login", passive_deletes=True)

    def __repr__(self):
        return f"<Login(id_usuario={self.id_usuario})>"
