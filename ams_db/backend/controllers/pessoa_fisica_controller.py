from flask import Blueprint, request, jsonify
from backend.schemas.pessoa_fisica_schema import (
    PessoaFisicaCreateSchema,
    PessoaFisicaResponseSchema,
    PessoaFisicaUpdateSchema
)
from backend.services.pessoa_fisica_service import (
    criar_pessoa_fisica, buscar_pessoa_fisica,
    atualizar_pessoa_fisica, deletar_pessoa_fisica
)
from backend.middlewares.auth_middleware import auth_required

pessoa_fisica_bp = Blueprint('pessoa_fisica', __name__)

# 🔹 Criar pessoa física
@pessoa_fisica_bp.route("/pessoas-fisicas", methods=["POST"])
def post_pessoa_fisica():
    dados_dict = request.get_json()
    dados_dict["id_usuario"] = int(dados_dict.get("id_usuario"))  # garante que é inteiro

    dados = PessoaFisicaCreateSchema(**dados_dict)
    pessoa_fisica = criar_pessoa_fisica(dados.model_dump())
    resposta = PessoaFisicaResponseSchema.model_validate(pessoa_fisica).model_dump()
    return jsonify(resposta), 201

# 🔹 Buscar pessoa física por id_usuario
@pessoa_fisica_bp.route("/pessoas-fisicas/<int:id_usuario>", methods=["GET"])
def get_pessoa_fisica(id_usuario):
    pessoa_fisica = buscar_pessoa_fisica(id_usuario)
    if pessoa_fisica:
        resposta = PessoaFisicaResponseSchema.model_validate(pessoa_fisica).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Pessoa física não encontrada"}), 404

# 🔹 Atualizar parcialmente pessoa física (sem permitir update de id_usuario)
@pessoa_fisica_bp.route("/pessoas-fisicas/<int:id_usuario>", methods=["PUT"])
@auth_required
def put_pessoa_fisica(id_usuario):
    dados = PessoaFisicaUpdateSchema(**request.json)
    pessoa_fisica = atualizar_pessoa_fisica(id_usuario, dados.model_dump(exclude_unset=True))
    if pessoa_fisica:
        resposta = PessoaFisicaResponseSchema.model_validate(pessoa_fisica).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Pessoa física não encontrada"}), 404

# 🔹 Excluir pessoa física
@pessoa_fisica_bp.route("/pessoas-fisicas/<int:id_usuario>", methods=["DELETE"])
@auth_required
def delete_pessoa_fisica(id_usuario):
    pessoa_fisica = deletar_pessoa_fisica(id_usuario)
    if pessoa_fisica:
        return jsonify({"message": "Pessoa física excluída com sucesso"})
    return jsonify({"message": "Pessoa física não encontrada"}), 404
