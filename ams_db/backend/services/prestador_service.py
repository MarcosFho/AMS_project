from sqlalchemy.orm import joinedload
from backend.models.prestador_model import Prestador
from backend.config.session import get_db

# 🔹 Criar um novo prestador
def criar_prestador(dados_prestador):
    with get_db() as db:
        # ✅ Verifica se já existe prestador para este usuário
        existe = db.query(Prestador).filter(Prestador.id_usuario == dados_prestador["id_usuario"]).first()
        if existe:
            raise ValueError("Usuário já possui um cadastro de prestador.")

        prestador = Prestador(**dados_prestador)
        db.add(prestador)
        db.commit()              # ✅ grava no banco
        db.refresh(prestador)
        return prestador

# 🔹 Listar todos os prestadores
def listar_prestadores():
    with get_db() as db:
        return db.query(Prestador).options(joinedload(Prestador.usuario)).all()

# 🔹 Buscar prestador pelo ID (da tabela prestador)
def buscar_prestador(id):
    with get_db() as db:
        return db.query(Prestador).filter(Prestador.id == id).first()
    
# 🔹 Buscar prestador pelo ID do usuário (foreign key)
def buscar_prestador_por_usuario(id_usuario):
    with get_db() as db:
        return db.query(Prestador).filter(Prestador.id_usuario == id_usuario).first()

# 🔹 Atualizar um prestador pelo ID
def atualizar_prestador(id, dados_prestador):
    with get_db() as db:
        prestador = db.query(Prestador).filter(Prestador.id == id).first()
        if prestador:
            for key, value in dados_prestador.items():
                setattr(prestador, key, value)
            db.commit()          # ✅ confirma atualização
            db.refresh(prestador)
        return prestador

# 🔹 Excluir prestador
def deletar_prestador(id):
    with get_db() as db:
        prestador = db.query(Prestador).filter(Prestador.id == id).first()
        if prestador:
            db.delete(prestador)
            db.commit()          # ✅ confirma exclusão
        return prestador

# 🔹 Listar top N prestadores por avaliação
def listar_top_prestadores(limite=5):
    with get_db() as db:
        return (
            db.query(Prestador)
            .order_by(Prestador.avaliacao_media.desc())
            .limit(limite)
            .all()
        )
