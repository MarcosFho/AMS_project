from flask import Blueprint, request, jsonify
from backend.schemas.fazenda_foto_schema import (
    FazendaFotoCreateSchema, FazendaFotoResponseSchema, FazendaFotoUpdateSchema
)
from backend.services.fazenda_foto_service import (
    criar_fazenda_foto, listar_fotos_fazenda,
    atualizar_fazenda_foto, deletar_foto_fazenda
)
import os
from werkzeug.utils import secure_filename
from backend.middlewares.auth_middleware import auth_required

fazenda_foto_bp = Blueprint('fazenda_foto', __name__)

UPLOAD_FOLDER = "uploads/fazenda_fotos"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extensao_permitida(nome_arquivo):
    return "." in nome_arquivo and nome_arquivo.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# 🔹 Adicionar foto à fazenda com URL acessível publicamente
@fazenda_foto_bp.route("/fazendas/<int:id_fazenda>/fotos", methods=["POST"])
def post_fazenda_foto(id_fazenda):
    if "foto" not in request.files:
        return jsonify({"erro": "Arquivo 'foto' não encontrado"}), 400

    arquivo = request.files["foto"]
    descricao = request.form.get("descricao", "")

    if not extensao_permitida(arquivo.filename):
        return jsonify({"erro": "Extensão de arquivo não permitida (somente .jpg, .jpeg, .png)"}), 400

    filename = secure_filename(arquivo.filename)
    caminho_completo = os.path.join(UPLOAD_FOLDER, filename)
    arquivo.save(caminho_completo)

    url_acessivel = f"http://localhost:5000/{UPLOAD_FOLDER}/{filename}"

    dados = {
        "id_fazenda": id_fazenda,
        "url_foto": url_acessivel,
        "descricao": descricao
    }

    foto = criar_fazenda_foto(dados)
    resposta = FazendaFotoResponseSchema.model_validate(foto).model_dump()
    return jsonify(resposta), 201

# 🔹 Listar fotos de uma fazenda
@fazenda_foto_bp.route("/fazendas/<int:id_fazenda>/fotos", methods=["GET"])
def get_fazenda_fotos(id_fazenda):
    fotos = listar_fotos_fazenda(id_fazenda)
    return jsonify([
        FazendaFotoResponseSchema.model_validate(f).model_dump()
        for f in fotos
    ])

# 🔹 Atualizar foto da fazenda
@fazenda_foto_bp.route("/fazendas/fotos/<int:id>", methods=["PUT"])
@auth_required
def put_fazenda_foto(id):
    dados = FazendaFotoUpdateSchema(**request.json)
    dados_dict = dados.dict(exclude_unset=True)
    foto = atualizar_fazenda_foto(id, dados_dict)
    if foto:
        resposta = FazendaFotoResponseSchema.model_validate(foto).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Foto de fazenda não encontrada"}), 404

# 🔹 Deletar foto da fazenda
@fazenda_foto_bp.route("/fazendas/fotos/<int:id>", methods=["DELETE"])
@auth_required
def delete_fazenda_foto(id):
    foto = deletar_foto_fazenda(id)
    if foto:
        return jsonify({"message": "Foto de fazenda excluída com sucesso"})
    return jsonify({"message": "Foto de fazenda não encontrada"}), 404
