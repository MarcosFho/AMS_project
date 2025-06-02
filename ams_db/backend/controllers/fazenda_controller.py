from flask import Blueprint, request, jsonify
from backend.schemas.fazenda_schema import (
    FazendaCreateSchema, FazendaResponseSchema, FazendaUpdateSchema
)
from backend.models.fazenda_model import Fazenda
from backend.models.fazenda_foto_model import FazendaFoto
from backend.services.fazenda_service import (
    criar_fazenda, listar_fazendas_filtradas,
    buscar_fazenda, atualizar_fazenda, deletar_fazenda
)
from backend.config.session import get_db
from backend.middlewares.auth_middleware import auth_required
from werkzeug.utils import secure_filename
from datetime import datetime
import os

fazenda_bp = Blueprint("fazenda", __name__)
UPLOAD_FOLDER = "./static/uploads/fazendas"

# 🔹 Criar uma nova fazenda
@fazenda_bp.route("/api/fazendas", methods=["POST"])
@auth_required
def post_fazenda():
    form = request.form
    arquivos = request.files.getlist("fotos")

    if len(arquivos) > 6:
        return jsonify({"erro": "Você pode enviar no máximo 6 fotos."}), 400

    dados_dict = {
        "nome": form.get("nome"),
        "descricao": form.get("descricao"),
        "telefone": form.get("telefone"),
        "area_total": float(form.get("area_total")) if form.get("area_total") else None,
        "tipo_atividade": form.get("tipo_atividade"),
        "localizacao": form.get("localizacao"),
        "id_endereco": int(form.get("id_endereco")) if form.get("id_endereco") else None,
        "id_usuario": int(request.usuario_id),
    }

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    with get_db() as db:
        fazenda = criar_fazenda(dados_dict, db)

        for foto in arquivos:
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
            nome_arquivo = secure_filename(f"{timestamp}_{foto.filename}")
            caminho_local = os.path.join(UPLOAD_FOLDER, nome_arquivo)
            foto.save(caminho_local)

            caminho_web = f"/uploads/fazendas/{nome_arquivo}"

            foto_fazenda = FazendaFoto(
                id_fazenda=fazenda.id,
                url_foto=caminho_web
            )
            db.add(foto_fazenda)

        db.commit()

        fazenda.fotos = db.query(FazendaFoto).filter_by(id_fazenda=fazenda.id).all()
        resposta = FazendaResponseSchema.model_validate(fazenda).model_dump()
        return jsonify(resposta), 201

# 🔹 Listar todas as fazendas
@fazenda_bp.route("/api/fazendas", methods=["GET"])
def get_fazendas():
    tipo_atividade = request.args.get("tipo_atividade")
    localizacao = request.args.get("localizacao")

    with get_db() as db:
        fazendas = listar_fazendas_filtradas(db, tipo_atividade=tipo_atividade, localizacao=localizacao)
        resultado = []

        for fazenda in fazendas:
            fazenda.fotos = db.query(FazendaFoto).filter_by(id_fazenda=fazenda.id).all()
            fazenda_dict = FazendaResponseSchema.model_validate(fazenda).model_dump()
            resultado.append(fazenda_dict)

        return jsonify(resultado), 200

# 🔹 Buscar fazenda por ID
@fazenda_bp.route("/api/fazendas/<int:id>", methods=["GET"])
def get_fazenda(id):
    with get_db() as db:
        fazenda = buscar_fazenda(id, db)
        if not fazenda:
            return jsonify({"message": "Fazenda não encontrada"}), 404

        fazenda.fotos = db.query(FazendaFoto).filter_by(id_fazenda=id).all()
        resposta = FazendaResponseSchema.model_validate(fazenda).model_dump()
        return jsonify(resposta)

# 🔹 Atualizar uma fazenda
@fazenda_bp.route("/api/fazendas/<int:id>", methods=["PUT"])
@auth_required
def put_fazenda(id):
    dados = FazendaUpdateSchema(**request.json)
    dados_dict = dados.model_dump(exclude_unset=True)

    with get_db() as db:
        fazenda = atualizar_fazenda(id, dados_dict, db)
        if fazenda:
            fazenda.fotos = db.query(FazendaFoto).filter_by(id_fazenda=id).all()
            resposta = FazendaResponseSchema.model_validate(fazenda).model_dump()
            return jsonify(resposta)

        return jsonify({"message": "Fazenda não encontrada"}), 404

# 🔹 Excluir uma fazenda
@fazenda_bp.route("/api/fazendas/<int:id>", methods=["DELETE"])
@auth_required
def delete_fazenda(id):
    with get_db() as db:
        fazenda = deletar_fazenda(id, db)
        if fazenda:
            return jsonify({"message": "Fazenda excluída com sucesso"})
        return jsonify({"message": "Fazenda não encontrada"}), 404

# 🔹 Adicionar foto avulsa à fazenda
@fazenda_bp.route("/api/fazendas/<int:id_fazenda>/fotos", methods=["POST"])
@auth_required
def post_fazenda_foto(id_fazenda):
    dados = request.get_json()
    url_foto = dados.get("url_foto")

    if not url_foto:
        return jsonify({"erro": "URL da foto é obrigatória"}), 400

    with get_db() as db:
        foto = FazendaFoto(id_fazenda=id_fazenda, url_foto=url_foto)
        db.add(foto)
        db.commit()

    return jsonify({"mensagem": "Foto adicionada com sucesso!"}), 201
