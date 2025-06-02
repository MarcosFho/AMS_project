from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.config.database import Base

class PessoaJuridica(Base):
    __tablename__ = 'pessoa_juridica'

    id_usuario = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), primary_key=True)
    razao_social = Column(String(150), nullable=False)
    cnpj = Column(String(18), nullable=False, unique=True)
    cnae = Column(String(20))
    inscricao_estadual = Column(String(20))

    # 🔁 Relacionamento com Usuario
    usuario = relationship("Usuario", backref="pessoa_juridica", passive_deletes=True)

    def __repr__(self):
        return f"<PessoaJuridica(id_usuario={self.id_usuario}, razao_social='{self.razao_social}')>"
