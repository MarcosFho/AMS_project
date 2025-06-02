from flask import Blueprint, request, jsonify
from backend.schemas.pessoa_juridica_schema import (
    PessoaJuridicaCreateSchema, PessoaJuridicaUpdateSchema, PessoaJuridicaResponseSchema
)
from backend.services.pessoa_juridica_service import (
    criar_pessoa_juridica, buscar_pessoa_juridica,
    atualizar_pessoa_juridica, deletar_pessoa_juridica
)
from backend.middlewares.auth_middleware import auth_required

pessoa_juridica_bp = Blueprint('pessoa_juridica', __name__)

# 🔹 Criar pessoa jurídica
@pessoa_juridica_bp.route("/api/pessoas-juridicas", methods=["POST"])
def post_pessoa_juridica():
    dados_dict = request.get_json()  # ← pega os dados enviados via JSON
    dados = PessoaJuridicaCreateSchema(**dados_dict)  # ← valida com schema
    pessoa_juridica = criar_pessoa_juridica(dados.dict())  # ← chama service
    resposta = PessoaJuridicaResponseSchema.model_validate(pessoa_juridica).model_dump()
    return jsonify(resposta), 201

# 🔹 Buscar pessoa jurídica por id_usuario
@pessoa_juridica_bp.route("/api/pessoas-juridicas/<int:id_usuario>", methods=["GET"])
def get_pessoa_juridica(id_usuario):
    pessoa_juridica = buscar_pessoa_juridica(id_usuario)
    if pessoa_juridica:
        resposta = PessoaJuridicaResponseSchema.model_validate(pessoa_juridica).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Pessoa jurídica não encontrada"}), 404

# 🔹 Atualizar pessoa jurídica (parcial)
@pessoa_juridica_bp.route("/api/pessoas-juridicas/<int:id_usuario>", methods=["PUT"])
@auth_required
def put_pessoa_juridica(id_usuario):
    dados = PessoaJuridicaUpdateSchema(**request.json)
    pessoa_juridica = atualizar_pessoa_juridica(id_usuario, dados.model_dump(exclude_unset=True))
    if pessoa_juridica:
        resposta = PessoaJuridicaResponseSchema.model_validate(pessoa_juridica).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Pessoa jurídica não encontrada"}), 404

# 🔹 Excluir pessoa jurídica
@pessoa_juridica_bp.route("/api/pessoas-juridicas/<int:id_usuario>", methods=["DELETE"])
@auth_required
def delete_pessoa_juridica(id_usuario):
    pessoa_juridica = deletar_pessoa_juridica(id_usuario)
    if pessoa_juridica:
        return jsonify({"message": "Pessoa jurídica excluída com sucesso"})
    return jsonify({"message": "Pessoa jurídica não encontrada"}), 404
