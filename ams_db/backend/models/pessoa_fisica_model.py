from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.config.database import Base

class PessoaFisica(Base):
    __tablename__ = 'pessoa_fisica'

    id_usuario = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), primary_key=True)
    cpf = Column(String(14), nullable=False, unique=True)
    rg = Column(String(20))
    data_nascimento = Column(Date)

    # 🔁 Relacionamento com Usuario
    usuario = relationship("Usuario", backref="pessoa_fisica", passive_deletes=True)

    def __repr__(self):
        return f"<PessoaFisica(id_usuario={self.id_usuario}, cpf='{self.cpf}')>"
