from backend.models.solicitacao_model import Solicitacao
from backend.config.session import get_db

# 🔹 Criar uma nova solicitação
def criar_solicitacao(id_usuario: int, id_servico: int):
    with get_db() as db:
        solicitacao = Solicitacao(id_usuario=id_usuario, id_servico=id_servico)
        db.add(solicitacao)
        db.commit()              # ✅ grava no banco
        db.refresh(solicitacao)
        return solicitacao

# 🔹 Listar solicitações de um usuário
def listar_solicitacoes_por_usuario(id_usuario: int):
    with get_db() as db:
        return db.query(Solicitacao).filter(Solicitacao.id_usuario == id_usuario).all()

# 🔹 Alterar status da solicitação (aceitar, recusar, etc.)
def atualizar_status_solicitacao(id: int, novo_status: str):
    with get_db() as db:
        solicitacao = db.query(Solicitacao).filter(Solicitacao.id == id).first()
        if solicitacao:
            solicitacao.status = novo_status
            db.commit()          # ✅ confirma alteração de status
            db.refresh(solicitacao)
        return solicitacao
