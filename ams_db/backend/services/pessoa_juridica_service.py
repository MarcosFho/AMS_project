from backend.models.pessoa_juridica_model import PessoaJuridica
from backend.config.session import get_db

# 🔹 Criar pessoa jurídica
def criar_pessoa_juridica(dados_pj):
    with get_db() as db:
        pj = PessoaJuridica(**dados_pj)
        db.add(pj)
        db.commit()              # ✅ grava no banco
        db.refresh(pj)
        return pj

# 🔹 Buscar pessoa jurídica pelo ID de usuário
def buscar_pessoa_juridica(id_usuario):
    with get_db() as db:
        return db.query(PessoaJuridica).filter(PessoaJuridica.id_usuario == id_usuario).first()

# 🔹 Atualizar pessoa jurídica
def atualizar_pessoa_juridica(id_usuario, dados_pj):
    with get_db() as db:
        pj = db.query(PessoaJuridica).filter(PessoaJuridica.id_usuario == id_usuario).first()
        if pj:
            for key, value in dados_pj.items():
                setattr(pj, key, value)
            db.commit()          # ✅ confirma atualização
            db.refresh(pj)
        return pj

# 🔹 Excluir pessoa jurídica
def deletar_pessoa_juridica(id_usuario):
    with get_db() as db:
        pj = db.query(PessoaJuridica).filter(PessoaJuridica.id_usuario == id_usuario).first()
        if pj:
            db.delete(pj)
            db.commit()          # ✅ confirma exclusão
        return pj
