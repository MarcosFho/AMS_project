from backend.models.pessoa_fisica_model import PessoaFisica
from backend.config.session import get_db

# 🔹 Criar pessoa física
def criar_pessoa_fisica(dados_pf):
    with get_db() as db:
        pf = PessoaFisica(**dados_pf)
        db.add(pf)
        db.commit()              # ✅ grava no banco
        db.refresh(pf)
        return pf

# 🔹 Buscar pessoa física pelo ID de usuário
def buscar_pessoa_fisica(id_usuario):
    with get_db() as db:
        return db.query(PessoaFisica).filter(PessoaFisica.id_usuario == id_usuario).first()

# 🔹 Atualizar pessoa física
def atualizar_pessoa_fisica(id_usuario, dados_pf):
    with get_db() as db:
        pf = db.query(PessoaFisica).filter(PessoaFisica.id_usuario == id_usuario).first()
        if pf:
            for key, value in dados_pf.items():
                setattr(pf, key, value)
            db.commit()          # ✅ confirma atualização
            db.refresh(pf)
        return pf

# 🔹 Excluir pessoa física
def deletar_pessoa_fisica(id_usuario):
    with get_db() as db:
        pf = db.query(PessoaFisica).filter(PessoaFisica.id_usuario == id_usuario).first()
        if pf:
            db.delete(pf)
            db.commit()          # ✅ confirma exclusão
        return pf
