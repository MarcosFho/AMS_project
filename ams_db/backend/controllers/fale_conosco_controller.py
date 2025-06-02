from flask import Blueprint, request, jsonify
from backend.schemas.fale_conosco_schema import FaleConoscoCreateSchema, FaleConoscoResponseSchema
from backend.services.fale_conosco_service import (
    criar_fale_conosco, listar_fale_conosco,
    buscar_fale_conosco, deletar_fale_conosco
)
from backend.middlewares.auth_middleware import auth_required
from pydantic import ValidationError

fale_conosco_bp = Blueprint('fale_conosco', __name__)

# 🔹 Criar nova mensagem de fale conosco
@fale_conosco_bp.route("/fale-conosco", methods=["POST"])
@auth_required  # 🔐 Protege a rota com autenticação
def post_fale_conosco():
    try:
        # Valida os dados recebidos
        dados = FaleConoscoCreateSchema(**request.json)
        dados_dict = dados.model_dump()
        
        # Adiciona o ID do usuário autenticado
        dados_dict["id_usuario"] = int(request.usuario_id)

        # Cria a mensagem
        mensagem = criar_fale_conosco(dados_dict)
        resposta = FaleConoscoResponseSchema.model_validate(mensagem).model_dump()
        return jsonify(resposta), 201
        
    except ValidationError as e:
        # Erro de validação do Pydantic
        return jsonify({"erro": "Dados inválidos", "detalhes": e.errors()}), 400
    except Exception as e:
        # Outros erros
        return jsonify({"erro": str(e)}), 400

# 🔹 Listar todas as mensagens de fale conosco
@fale_conosco_bp.route("/fale-conosco", methods=["GET"])
@auth_required  # 🔐 Protege a rota com autenticação
def listar_fale_conosco_route():
    mensagens = listar_fale_conosco()
    return jsonify([
        FaleConoscoResponseSchema.model_validate(m).model_dump()
        for m in mensagens
    ])

# 🔹 Buscar mensagem por ID
@fale_conosco_bp.route("/fale-conosco/<int:id>", methods=["GET"])
@auth_required  # 🔐 Protege a rota com autenticação
def buscar_fale_conosco_route(id):
    mensagem = buscar_fale_conosco(id)
    if mensagem:
        resposta = FaleConoscoResponseSchema.model_validate(mensagem).model_dump()
        return jsonify(resposta)
    return jsonify({"message": "Mensagem não encontrada"}), 404

# 🔹 Excluir mensagem por ID
@fale_conosco_bp.route("/fale-conosco/<int:id>", methods=["DELETE"])
@auth_required
def delete_fale_conosco(id):
    mensagem = deletar_fale_conosco(id)
    if mensagem:
        return jsonify({"message": "Mensagem excluída com sucesso"})
    return jsonify({"message": "Mensagem não encontrada"}), 404
