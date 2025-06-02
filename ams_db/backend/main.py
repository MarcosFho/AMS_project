import os
import sys

# 🧭 Garante que o Python encontre todos os módulos corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, send_from_directory, abort
from flask_cors import CORS
from dotenv import load_dotenv

# Ajusta o caminho para encontrar o arquivo .env na raiz do projeto
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
env_path = os.path.join(root_dir, ".env")

# 📦 Carrega variáveis de ambiente
load_dotenv(env_path)

from backend.routes.api import registrar_rotas
from backend.middlewares.error_handler import register_error_handlers
from backend.config.database import init_db

# 🚀 Inicializa o app Flask
app = Flask(__name__)

# 🌐 CORS para permitir chamadas da web frontend nas rotas /api/*
CORS(app,
     resources={r"/api/*": {"origins": ["http://localhost:5173", "http://localhost:5174"]}},
     supports_credentials=True,
     expose_headers=["Content-Type", "Authorization"],
     allow_headers=["Content-Type", "Authorization"])

# 🔐 Configurações sensíveis
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fallback-secret")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limite upload

# 🛣️ Registra rotas e middlewares personalizados
registrar_rotas(app)
register_error_handlers(app)

@app.after_request
def after_request(response):
    return response

# 📂 Endpoint para servir arquivos estáticos (incluindo subpastas)
@app.route("/uploads/<path:filename>")
def servir_arquivo_estatico(filename):
    UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "static", "uploads"))
    caminho_arquivo = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.isfile(caminho_arquivo):
        return {"erro": "Recurso não encontrado"}, 404
    return send_from_directory(UPLOAD_FOLDER, filename)

# 🌱 Rota principal
@app.route("/")
def home():
    return "AMS - Agro Marketing Service - Plataforma de intermediação entre fazendeiros e prestadores de serviço"

# ▶️ Executa o servidor
if __name__ == "__main__":
    # Inicializa o banco de dados
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
