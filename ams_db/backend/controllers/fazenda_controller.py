from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from backend.schemas.fazenda_schema import (
    FazendaCreateSchema, FazendaResponseSchema, FazendaUpdateSchema
)
from backend.services.fazenda_service import (
    criar_fazenda, listar_fazendas, buscar_fazenda,
    atualizar_fazenda, deletar_fazenda
)
from backend.middlewares.auth_middleware import auth_required
from backend.models.fazenda_model import Fazenda
from backend.config.session import get_db

fazenda_bp = Blueprint('fazenda', __name__)

# 🔹 Criar uma nova fazenda
@fazenda_bp.route("/fazendas", methods=["POST"])
@auth_required
def post_fazenda():
    dados_dict = {
        "nome": request.form.get("nome"),
        "telefone": request.form.get("telefone"),
        "descricao": request.form.get("descricao"),
        "area_total": None,
        "localizacao": request.form.get("localizacao"),
        "tipo_atividade": request.form.get("tipo_atividade"),
        "id_usuario": int(request.usuario_id),
    }
    area_total_str = request.form.get("area_total")
    if area_total_str:
        area_total_str = area_total_str.replace(",", ".")
        try:
            dados_dict["area_total"] = float(area_total_str)
        except Exception:
            dados_dict["area_total"] = None

    fotos = request.files.getlist("fotos")
    fazenda_id = criar_fazenda(dados_dict, fotos)  # agora retorna só o id

    with get_db() as db:
        fazenda_db = db.query(Fazenda).options(joinedload(Fazenda.fotos)).filter(Fazenda.id == fazenda_id).first()
        resposta = FazendaResponseSchema.model_validate(fazenda_db).model_dump()
    return jsonify(resposta), 201

# 🔹 Listar todas as fazendas
@fazenda_bp.route("/fazendas", methods=["GET"])
def get_fazendas():
    with get_db() as db:
        fazendas_db = db.query(Fazenda).options(joinedload(Fazenda.fotos)).all()
        return jsonify([
            FazendaResponseSchema.model_validate(f).model_dump()
            for f in fazendas_db
        ])

# 🔹 Buscar fazenda por ID
@fazenda_bp.route("/fazendas/<int:id>", methods=["GET"])
def get_fazenda(id):
    with get_db() as db:
        fazenda = db.query(Fazenda).options(joinedload(Fazenda.fotos)).filter(Fazenda.id == id).first()
        if fazenda:
            resposta = FazendaResponseSchema.model_validate(fazenda).model_dump()
            return jsonify(resposta)
    return jsonify({"message": "Fazenda não encontrada"}), 404

# 🔹 Atualizar fazenda por ID
@fazenda_bp.route("/fazendas/<int:id>", methods=["PUT"])
@auth_required
def put_fazenda(id):
    # Checa se está vindo como form-data ou JSON
    if request.content_type and request.content_type.startswith("multipart/form-data"):
        # Recebendo via form (com ou sem fotos)
        dados_dict = {
            "nome": request.form.get("nome"),
            "telefone": request.form.get("telefone"),
            "descricao": request.form.get("descricao"),
            "area_total": None,
            "localizacao": request.form.get("localizacao"),
            "tipo_atividade": request.form.get("tipo_atividade"),
        }
        area_total_str = request.form.get("area_total")
        if area_total_str:
            area_total_str = area_total_str.replace(",", ".")
            try:
                dados_dict["area_total"] = float(area_total_str)
            except Exception:
                dados_dict["area_total"] = None

        fotos = request.files.getlist("fotos")
    else:
        # Recebendo via JSON puro
        dados = FazendaUpdateSchema(**request.json)
        dados_dict = dados.dict(exclude_unset=True)
        fotos = None

    # Atualiza fazenda e fotos (adapte o service para lidar com update de fotos se precisar)
    fazenda_id = atualizar_fazenda(id, dados_dict, fotos)
    if fazenda_id:
        with get_db() as db:
            fazenda = db.query(Fazenda).options(joinedload(Fazenda.fotos)).filter(Fazenda.id == id).first()
            if fazenda:
                resposta = FazendaResponseSchema.model_validate(fazenda).model_dump()
                return jsonify(resposta)
    return jsonify({"message": "Fazenda não encontrada"}), 404


# 🔹 Excluir fazenda por ID
@fazenda_bp.route("/fazendas/<int:id>", methods=["DELETE"])
@auth_required
def delete_fazenda(id):
    success = deletar_fazenda(id)
    if success:
        return jsonify({"message": "Fazenda excluída com sucesso"})
    return jsonify({"message": "Fazenda não encontrada"}), 404
