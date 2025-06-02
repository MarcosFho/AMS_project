from flask import Blueprint, request, jsonify
from backend.schemas.servico_foto_schema import (
    ServicoFotoCreateSchema, ServicoFotoResponseSchema, ServicoFotoUpdateSchema
)
from backend.services.servico_foto_service import (
    criar_servico_foto, listar_fotos_servico,
    deletar_foto_servico, atualizar_servico_foto, buscar_servico_foto
)
import os
from werkzeug.utils import secure_filename
from backend.middlewares.auth_middleware import auth_required

servico_foto_bp = Blueprint('servico_foto', __name__)

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static", "uploads", "servico_fotos"))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

def extensao_permitida(nome_arquivo):
    return "." in nome_arquivo and nome_arquivo.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# 🔹 Upload de uma foto (com URL pública acessível)
@servico_foto_bp.route("/servicos/<int:id_servico>/fotos", methods=["POST"])
@auth_required
def post_servico_foto(id_servico):
    if "foto" not in request.files:
        return jsonify({"erro": "Arquivo 'foto' não encontrado"}), 400

    arquivo = request.files["foto"]
    descricao = request.form.get("descricao", "")

    if not extensao_permitida(arquivo.filename):
        return jsonify({"erro": "Extensão de arquivo não permitida (somente jpg, jpeg, png)"}), 400

    filename = secure_filename(arquivo.filename)
    caminho_completo = os.path.join(UPLOAD_FOLDER, filename)
    arquivo.save(caminho_completo)

    url_acessivel = f"/uploads/servico_fotos/{filename}"

    dados = {
        "id_servico": id_servico,
        "url_foto": url_acessivel,
        "descricao": descricao
    }

    foto = criar_servico_foto(dados)
    resposta = ServicoFotoResponseSchema.model_validate(foto).model_dump()
    return jsonify(resposta), 201

# 🔹 Listar fotos de um serviço
@servico_foto_bp.route("/servicos/<int:id_servico>/fotos", methods=["GET"])
def get_servico_fotos(id_servico):
    fotos = listar_fotos_servico(id_servico)
    return jsonify([
        ServicoFotoResponseSchema.model_validate(f).model_dump()
        for f in fotos
    ])

# 🔹 Atualizar foto de serviço (somente descrição ou url_foto, nunca id_servico)
@servico_foto_bp.route("/servicos/fotos/<int:id>", methods=["PUT"])
@auth_required
def put_servico_foto(id):
    foto = buscar_servico_foto(id)
    if not foto:
        return jsonify({"message": "Foto de serviço não encontrada"}), 404

    dados = ServicoFotoUpdateSchema(**request.json)
    atualizada = atualizar_servico_foto(id, dados.model_dump(exclude_unset=True))
    resposta = ServicoFotoResponseSchema.model_validate(atualizada).model_dump()
    return jsonify(resposta)

# 🔹 Deletar foto de serviço
@servico_foto_bp.route("/servicos/fotos/<int:id>", methods=["DELETE"])
@auth_required
def delete_servico_foto(id):
    foto = deletar_foto_servico(id)
    if foto:
        return jsonify({"message": "Foto de serviço excluída com sucesso"})
    return jsonify({"message": "Foto de serviço não encontrada"}), 404
