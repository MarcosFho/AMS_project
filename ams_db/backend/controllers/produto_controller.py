from flask import Blueprint, request, jsonify
from backend.schemas.produto_schema import (
    ProdutoCreateSchema, ProdutoResponseSchema, ProdutoUpdateSchema
)
from backend.services.produto_service import (
    criar_produto, listar_produtos, buscar_produto,
    atualizar_produto, deletar_produto
)
from backend.middlewares.auth_middleware import auth_required

produto_bp = Blueprint('produto', __name__)

# 🔹 Criar produto
@produto_bp.route("/produtos", methods=["POST"])
def post_produto():
    dados = ProdutoCreateSchema(**request.json)
    produto = criar_produto(dados.dict())
    resposta = ProdutoResponseSchema.model_validate(produto).model_dump()
    return jsonify(resposta), 201

# 🔹 Listar todos os produtos
@produto_bp.route("/produtos", methods=["GET"])
def get_produtos():
    produtos = listar_produtos()
    return jsonify([
        ProdutoResponseSchema.model_validate(p).model_dump()
        for p in produtos
    ])

# 🔹 Buscar produto por ID
@produto_bp.route("/produtos/<int:id>", methods=["GET"])
def get_produto(id):
    produto = buscar_produto(id)
    if produto:
        resposta = ProdutoResponseSchema.model_validate(produto).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Produto não encontrado"}), 404

# 🔹 Atualizar produto por ID
@produto_bp.route("/produtos/<int:id>", methods=["PUT"])
@auth_required
def put_produto(id):
    dados = ProdutoUpdateSchema(**request.json)
    dados_dict = dados.dict(exclude_unset=True)
    produto = atualizar_produto(id, dados_dict)
    if produto:
        resposta = ProdutoResponseSchema.model_validate(produto).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Produto não encontrado"}), 404

# 🔹 Excluir produto por ID
@produto_bp.route("/produtos/<int:id>", methods=["DELETE"])
@auth_required
def delete_produto(id):
    produto = deletar_produto(id)
    if produto:
        return jsonify({"message": "Produto excluído com sucesso"})
    return jsonify({"message": "Produto não encontrado"}), 404
