from flask import Blueprint, request, jsonify
from backend.schemas.servico_schema import (
    ServicoCreateSchema, ServicoResponseSchema, ServicoUpdateSchema, ServicoFotoSchema
)
from backend.models.servico_model import Servico
from backend.models.servico_foto_model import ServicoFoto
from backend.services.servico_service import (
    criar_servico, listar_servicos_filtrados,
    buscar_servico, atualizar_servico, deletar_servico
)
from backend.config.session import get_db
from backend.middlewares.auth_middleware import auth_required
import os
from sqlalchemy.orm import relationship

servico_bp = Blueprint('servico', __name__)

# 🔹 Criar um novo serviço
@servico_bp.route("/servicos", methods=["POST"])
@auth_required
def post_servico():
    form = request.form
    arquivos = request.files.getlist("fotos")

    if len(arquivos) > 6:
        return jsonify({"erro": "Você pode enviar no máximo 6 fotos."}), 400

    dados_dict = {
        "tipo": form.get("tipo"),
        "descricao": form.get("descricao"),
        "preco": float(form.get("preco")) if form.get("preco") else None,
        "categoria": form.get("categoria"),
        "localizacao": form.get("localizacao"),
        "id_usuario": int(request.usuario_id),
    }

    with get_db() as db:
        servico = criar_servico(dados_dict, db)

        for foto in arquivos:
            nome_arquivo = foto.filename
            pasta_destino = os.path.join(os.path.dirname(__file__), "..", "static", "uploads", "servico_fotos")
            pasta_destino = os.path.abspath(pasta_destino)
            os.makedirs(pasta_destino, exist_ok=True)
            caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
            foto.save(caminho_arquivo)
            caminho_url = f"/uploads/servico_fotos/{nome_arquivo}"

            servico_foto = ServicoFoto(
                id_servico=servico.id,
                url_foto=caminho_url
            )
            db.add(servico_foto)

        db.commit()

        servico.fotos = db.query(ServicoFoto).filter_by(id_servico=servico.id).all()
        resposta = ServicoResponseSchema.model_validate(servico).model_dump()
        return jsonify(resposta), 201

# 🔹 Listar todos os serviços
@servico_bp.route("/servicos", methods=["GET"])
def get_servicos():
    categoria = request.args.get("categoria")
    localizacao = request.args.get("localizacao")

    with get_db() as db:
        servicos = listar_servicos_filtrados(db, categoria=categoria, localizacao=localizacao)
        resultado = []

        for servico in servicos:
            servico.fotos = db.query(ServicoFoto).filter_by(id_servico=servico.id).all()
            servico_dict = ServicoResponseSchema.model_validate(servico).model_dump()
            resultado.append(servico_dict)

        return jsonify(resultado), 200

# 🔹 Buscar serviço por ID
@servico_bp.route("/servicos/<int:id>", methods=["GET"])
def get_servico(id):
    with get_db() as db:
        servico = buscar_servico(id, db)
        if not servico:
            return jsonify({"message": "Serviço não encontrado"}), 404

        servico.fotos = db.query(ServicoFoto).filter_by(id_servico=id).all()
        resposta = ServicoResponseSchema.model_validate(servico).model_dump()
        return jsonify(resposta)

# 🔹 Atualizar um serviço
@servico_bp.route("/servicos/<int:id>", methods=["PUT"])
@auth_required
def put_servico(id):
    dados = ServicoUpdateSchema(**request.json)
    dados_dict = dados.model_dump(exclude_unset=True)

    with get_db() as db:
        servico = db.query(Servico).filter(Servico.id == id).first()
        if not servico:
            return jsonify({"message": "Serviço não encontrado"}), 404
        if servico.id_usuario != request.usuario_id:
            return jsonify({"message": "Você não tem permissão para editar este serviço."}), 403
        servico = atualizar_servico(id, dados_dict, db)
        if servico:
            servico.fotos = db.query(ServicoFoto).filter_by(id_servico=id).all()
            resposta = ServicoResponseSchema.model_validate(servico).model_dump()
            return jsonify(resposta)
        return jsonify({"message": "Serviço não encontrado"}), 404

# 🔹 Excluir um serviço
@servico_bp.route("/servicos/<int:id>", methods=["DELETE"])
@auth_required
def delete_servico(id):
    with get_db() as db:
        servico = db.query(Servico).filter(Servico.id == id).first()
        if not servico:
            return jsonify({"message": "Serviço não encontrado"}), 404
        if servico.id_usuario != request.usuario_id:
            return jsonify({"message": "Você não tem permissão para excluir este serviço."}), 403
        db.query(ServicoFoto).filter(ServicoFoto.id_servico == id).delete(synchronize_session=False)
        servico = deletar_servico(id, db)
        if servico:
            return jsonify({"message": "Serviço excluído com sucesso"})
        return jsonify({"message": "Serviço não encontrado"}), 404

# 🔹 Adicionar foto avulsa
@servico_bp.route("/servicos/<int:id_servico>/fotos", methods=["POST"])
@auth_required
def post_servico_foto(id_servico):
    dados = request.get_json()
    url_foto = dados.get("url_foto")

    if not url_foto:
        return jsonify({"erro": "URL da foto é obrigatória"}), 400

    with get_db() as db:
        foto = ServicoFoto(id_servico=id_servico, url_foto=url_foto)
        db.add(foto)
        db.commit()

    return jsonify({"mensagem": "Foto adicionada com sucesso!"}), 201
