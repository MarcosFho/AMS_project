from backend.models.avaliacao_model import Avaliacao
from backend.models.servico_model import Servico
from backend.models.prestador_model import Prestador
from backend.config.session import get_db

# 🔹 Criar avaliação e atualizar média do prestador
def criar_avaliacao(id_cliente: int, dados):
    with get_db() as db:
        avaliacao = Avaliacao(
            id_cliente=id_cliente,
            id_servico=dados.id_servico,
            nota=dados.nota,
            comentario=dados.comentario
        )
        db.add(avaliacao)
        db.commit()
        db.refresh(avaliacao)

        # 🧠 Atualizar média do prestador
        servico = db.query(Servico).filter(Servico.id == dados.id_servico).first()
        if servico:
            id_prestador = servico.id_prestador
            notas = (
                db.query(Avaliacao.nota)
                .join(Servico, Avaliacao.id_servico == Servico.id)
                .filter(Servico.id_prestador == id_prestador)
                .all()
            )
            media = sum([n[0] for n in notas]) / len(notas)
            prestador = db.query(Prestador).filter(Prestador.id == id_prestador).first()
            prestador.avaliacao_media = round(media, 2)
            db.commit()

        # ✅ Extrai dados antes de fechar sessão
        resultado = {
            "id": avaliacao.id,
            "id_servico": avaliacao.id_servico,
            "id_cliente": avaliacao.id_cliente,
            "nota": avaliacao.nota,
            "comentario": avaliacao.comentario,
            "data_avaliacao": avaliacao.data_avaliacao
        }

        return resultado


# 🔹 Listar todas as avaliações
def listar_avaliacoes():
    with get_db() as db:
        return db.query(Avaliacao).all()

# 🔹 Buscar avaliação pelo ID
def buscar_avaliacao(id):
    with get_db() as db:
        return db.query(Avaliacao).filter(Avaliacao.id == id).first()

# 🔹 Excluir uma avaliação pelo ID
def deletar_avaliacao(id):
    with get_db() as db:
        avaliacao = db.query(Avaliacao).filter(Avaliacao.id == id).first()
        if avaliacao:
            db.delete(avaliacao)
            db.commit()          # ✅ confirma a exclusão
        return avaliacao
