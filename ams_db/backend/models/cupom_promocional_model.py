from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from backend.config.database import Base  # Corrige o import do seu projeto

class CupomPromocional(Base):
    __tablename__ = "cupom_promocional"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(50), unique=True, nullable=False)
    descricao = Column(String(255), nullable=True)
    desconto_percentual = Column(Float, nullable=False, default=0.0)
    data_expiracao = Column(DateTime, nullable=False)
    criado_em = Column(DateTime, server_default=func.now())  # ⏱ usa func.now() para compatibilidade com DBs

    def __repr__(self):
        return (
            f"<CupomPromocional(codigo='{self.codigo}', desconto={self.desconto_percentual}%, "
            f"expira_em={self.data_expiracao})>"
        )
