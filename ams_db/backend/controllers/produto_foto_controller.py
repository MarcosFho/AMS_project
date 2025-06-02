from flask import Blueprint, request, jsonify
from backend.schemas.produto_foto_schema import (
    ProdutoFotoResponseSchema,
    ProdutoFotoUpdateSchema
)
from backend.services.produto_foto_service import (
    criar_produto_foto, listar_fotos_produto,
    atualizar_produto_foto, deletar_foto_produto
)
from backend.middlewares.auth_middleware import auth_required
import os
from werkzeug.utils import secure_filename

produto_foto_bp = Blueprint('produto_foto', __name__)

UPLOAD_FOLDER = "uploads/produto_fotos"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extensao_permitida(nome_arquivo):
    return "." in nome_arquivo and nome_arquivo.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# 🔹 Adicionar foto ao produto via upload (com URL acessível)
@produto_foto_bp.route("/api/produtos/<int:id_produto>/fotos", methods=["POST"])
def post_produto_foto(id_produto):
    if "foto" not in request.files:
        return jsonify({"erro": "Arquivo 'foto' não encontrado"}), 400

    arquivo = request.files["foto"]
    descricao = request.form.get("descricao", "")

    if not extensao_permitida(arquivo.filename):
        return jsonify({"erro": "Extensão de arquivo não permitida (somente .jpg, .jpeg, .png)"}), 400

    filename = secure_filename(arquivo.filename)
    caminho_completo = os.path.join(UPLOAD_FOLDER, filename)
    arquivo.save(caminho_completo)

    # URL pública acessível
    url_acessivel = f"http://localhost:5000/{UPLOAD_FOLDER}/{filename}"

    dados = {
        "id_produto": id_produto,
        "url_foto": url_acessivel,
        "descricao": descricao
    }

    foto = criar_produto_foto(dados)
    resposta = ProdutoFotoResponseSchema.model_validate(foto).model_dump()
    return jsonify(resposta), 201

# 🔹 Listar fotos de um produto
@produto_foto_bp.route("/api/produtos/<int:id_produto>/fotos", methods=["GET"])
def get_produto_fotos(id_produto):
    fotos = listar_fotos_produto(id_produto)
    return jsonify([
        ProdutoFotoResponseSchema.model_validate(f).model_dump()
        for f in fotos
    ])

# 🔹 Atualizar uma foto de produto
@produto_foto_bp.route("/api/produtos/fotos/<int:id>", methods=["PUT"])
@auth_required
def put_produto_foto(id):
    dados = ProdutoFotoUpdateSchema(**request.json)
    foto = atualizar_produto_foto(id, dados.model_dump(exclude_unset=True))
    if foto:
        resposta = ProdutoFotoResponseSchema.model_validate(foto).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Foto de produto não encontrada"}), 404

# 🔹 Deletar foto de produto
@produto_foto_bp.route("/api/produtos/fotos/<int:id>", methods=["DELETE"])
@auth_required
def delete_produto_foto(id):
    foto = deletar_foto_produto(id)
    if foto:
        return jsonify({"message": "Foto de produto excluída com sucesso"})
    return jsonify({"message": "Foto de produto não encontrada"}), 404
