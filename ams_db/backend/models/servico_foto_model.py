from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.config.database import Base

class ServicoFoto(Base):
    __tablename__ = 'servico_foto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_servico = Column(Integer, ForeignKey("servico.id", ondelete="CASCADE"), nullable=False)
    url_foto = Column(String(255), nullable=False)
    descricao = Column(String(100))

    # 🔁 Relacionamento com Servico
    servico = relationship("Servico", backref="fotos", passive_deletes=True)

    def __repr__(self):
        return f"<ServicoFoto(id={self.id}, id_servico={self.id_servico}, url_foto='{self.url_foto}')>"
