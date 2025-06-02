from flask import Blueprint, request, jsonify
from backend.schemas.fazenda_schema import (
    FazendaCreateSchema, FazendaResponseSchema, FazendaUpdateSchema
)
from backend.services.fazenda_service import (
    criar_fazenda, listar_fazendas, buscar_fazenda,
    atualizar_fazenda, deletar_fazenda
)
from backend.middlewares.auth_middleware import auth_required

fazenda_bp = Blueprint('fazenda', __name__)

# 🔹 Criar uma nova fazenda
@fazenda_bp.route("/fazendas", methods=["POST"])
def post_fazenda():
    dados = FazendaCreateSchema(**request.json)
    dados_dict = dados.dict()

    dados_dict["id_usuario"] = int(request.usuario_id)  # 🔄 associar direto ao usuário

    fazenda = criar_fazenda(dados_dict)
    resposta = FazendaResponseSchema.model_validate(fazenda).model_dump()
    return jsonify(resposta), 201

# 🔹 Listar todas as fazendas
@fazenda_bp.route("/fazendas", methods=["GET"])
def get_fazendas():
    fazendas = listar_fazendas()
    return jsonify([
        FazendaResponseSchema.model_validate(f).model_dump()
        for f in fazendas
    ])

# 🔹 Buscar fazenda por ID
@fazenda_bp.route("/fazendas/<int:id>", methods=["GET"])
def get_fazenda(id):
    fazenda = buscar_fazenda(id)
    if fazenda:
        resposta = FazendaResponseSchema.model_validate(fazenda).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Fazenda não encontrada"}), 404

# 🔹 Atualizar fazenda por ID
@fazenda_bp.route("/fazendas/<int:id>", methods=["PUT"])
@auth_required
def put_fazenda(id):
    dados = FazendaUpdateSchema(**request.json)
    dados_dict = dados.dict(exclude_unset=True)
    fazenda = atualizar_fazenda(id, dados_dict)
    if fazenda:
        resposta = FazendaResponseSchema.model_validate(fazenda).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Fazenda não encontrada"}), 404

# 🔹 Excluir fazenda por ID
@fazenda_bp.route("/fazendas/<int:id>", methods=["DELETE"])
@auth_required
def delete_fazenda(id):
    fazenda = deletar_fazenda(id)
    if fazenda:
        return jsonify({"message": "Fazenda excluída com sucesso"})
    return jsonify({"message": "Fazenda não encontrada"}), 404
