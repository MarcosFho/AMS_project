from flask import Blueprint, request, jsonify
from backend.schemas.cliente_schema import ClienteCreateSchema, ClienteResponseSchema
from backend.services.cliente_service import (
    criar_cliente, listar_clientes, buscar_cliente_por_usuario,
    buscar_cliente, atualizar_cliente, deletar_cliente
)
from backend.middlewares.auth_middleware import auth_required
from backend.config.session import get_db
from backend.models.cliente_model import Cliente 

cliente_bp = Blueprint('cliente', __name__)

# 🔹 Criar um novo cliente
@cliente_bp.route("/clientes", methods=["POST"])
def post_cliente():
    dados = ClienteCreateSchema(**request.json)
    dados_dict = dados.dict()
    dados_dict["id_usuario"] = int(request.usuario_id)

    # ✅ Antes de criar, verifique se já existe cliente com esse usuário
    with get_db() as db:
        cliente_existente = db.query(Cliente).filter_by(id_usuario=dados_dict["id_usuario"]).first()
        if cliente_existente:
            return jsonify({"message": "Cliente já existe para este usuário"}), 409

    cliente = criar_cliente(dados_dict)
    resposta = ClienteResponseSchema.model_validate(cliente).model_dump()
    return jsonify(resposta), 201

# 🔹 Listar todos os clientes
@cliente_bp.route("/clientes", methods=["GET"])
def get_clientes():
    clientes = listar_clientes()
    return jsonify([
        ClienteResponseSchema.model_validate(c).model_dump()
        for c in clientes
    ])

# 🔹 Buscar cliente logado (perfil)
@cliente_bp.route("/clientes/perfil", methods=["GET"])
@auth_required
def get_me_cliente():
    usuario_id = int(request.usuario_id)
    cliente = buscar_cliente_por_usuario(usuario_id)
    if cliente:
        resposta = ClienteResponseSchema.model_validate(cliente).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Cliente não encontrado"}), 404

# 🔹 Buscar cliente por ID específico
@cliente_bp.route("/clientes/<int:id>", methods=["GET"])
@auth_required
def get_cliente(id):
    cliente = buscar_cliente(id)
    if cliente:
        resposta = ClienteResponseSchema.model_validate(cliente).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Cliente não encontrado"}), 404

# 🔹 Atualizar cliente por ID
@cliente_bp.route("/clientes/<int:id>", methods=["PUT"])
@auth_required
def put_cliente(id):
    dados = ClienteCreateSchema(**request.json)
    cliente = atualizar_cliente(id, dados.dict())
    if cliente:
        resposta = ClienteResponseSchema.model_validate(cliente).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Cliente não encontrado"}), 404

# 🔹 Excluir cliente por ID
@cliente_bp.route("/clientes/<int:id>", methods=["DELETE"])
@auth_required
def delete_cliente(id):
    cliente = deletar_cliente(id)
    if cliente:
        return jsonify({"message": "Cliente excluído com sucesso"})
    return jsonify({"message": "Cliente não encontrado"}), 404
