from flask import Blueprint, request, jsonify
from backend.schemas.prestador_schema import PrestadorCreateSchema, PrestadorResponseSchema, PrestadorUpdateSchema
from backend.services.prestador_service import (
    criar_prestador, listar_prestadores, buscar_prestador,
    atualizar_prestador, deletar_prestador, buscar_prestador_por_usuario, listar_top_prestadores
)
from middlewares.auth_middleware import auth_required

prestador_bp = Blueprint('prestador', __name__)

# 🔸 Função auxiliar para verificar se o prestador pertence ao usuário logado
def validar_proprietario(prestador, usuario_id):
    return prestador and prestador.id_usuario == usuario_id

# 🔹 Criar novo prestador
@prestador_bp.route("/prestadores", methods=["POST"])
def post_prestador():
    try:
        dados = PrestadorCreateSchema(**request.json)
        dados_dict = dados.dict()
        dados_dict["id_usuario"] = int(request.usuario_id)
        prestador = criar_prestador(dados_dict)
        resposta = PrestadorResponseSchema.model_validate(prestador).model_dump()
        return jsonify(resposta), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

# 🔹 Listar todos os prestadores
@prestador_bp.route("/prestadores", methods=["GET"])
def get_prestadores():
    prestadores = listar_prestadores()
    return jsonify([
        PrestadorResponseSchema.model_validate(p).model_dump()
        for p in prestadores
    ])

# 🔹 Buscar prestador por ID
@prestador_bp.route("/prestadores/<int:id>", methods=["GET"])
@auth_required
def get_prestador(id):
    prestador = buscar_prestador(id)
    if not validar_proprietario(prestador, int(request.usuario_id)):
        return jsonify({"message": "Prestador não encontrado"}), 404

    resposta = PrestadorResponseSchema.model_validate(prestador).model_dump()
    return jsonify(resposta)

# 🔹 Atualizar prestador por ID
@prestador_bp.route("/prestadores/<int:id>", methods=["PUT"])
@auth_required
def put_prestador(id):
    prestador = buscar_prestador(id)
    if not validar_proprietario(prestador, int(request.usuario_id)):
        return jsonify({"message": "Prestador não encontrado"}), 404

    dados = PrestadorUpdateSchema(**request.json)
    prestador = atualizar_prestador(id, dados.model_dump(exclude_unset=True))  # ✅ apenas campos enviados
    resposta = PrestadorResponseSchema.model_validate(prestador).model_dump()
    return jsonify(resposta)

# 🔹 Excluir prestador
@prestador_bp.route("/prestadores/<int:id>", methods=["DELETE"])
@auth_required
def delete_prestador(id):
    prestador = buscar_prestador(id)
    if not validar_proprietario(prestador, int(request.usuario_id)):
        return jsonify({"message": "Prestador não encontrado"}), 404

    deletar_prestador(id)
    return jsonify({"message": "Prestador excluído com sucesso"})

# 🔹 Buscar perfil do prestador logado
@prestador_bp.route("/prestadores/perfil", methods=["GET"])
@auth_required
def get_me_prestador():
    usuario_id = int(request.usuario_id)
    prestador = buscar_prestador_por_usuario(usuario_id)
    if prestador:
        resposta = PrestadorResponseSchema.model_validate(prestador).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Prestador não encontrado"}), 404

# 🔹 Listar prestadores com melhor avaliação
@prestador_bp.route("/prestadores/top", methods=["GET"])
def get_top_prestadores():
    limite = request.args.get("limite", default=5, type=int)
    prestadores = listar_top_prestadores(limite=limite)
    return jsonify([
        PrestadorResponseSchema.model_validate(p).model_dump()
        for p in prestadores
    ])
