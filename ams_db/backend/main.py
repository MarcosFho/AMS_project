import os
import sys

# 🧭 Garante que o Python encontre todos os módulos corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from backend.routes.api import registrar_rotas
from backend.middlewares.error_handler import register_error_handlers

# 📦 Carrega variáveis de ambiente
load_dotenv()

# 🚀 Inicializa o app Flask
app = Flask(__name__)

# 🌐 CORS para permitir chamadas da web frontend
CORS(app,
     resources={r"/api/*": {"origins": ["http://localhost:5173"]}},
     supports_credentials=True,
     expose_headers=["Content-Type", "Authorization"],
     allow_headers=["Content-Type", "Authorization"])


# 🔐 Configurações sensíveis
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fallback-secret")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

# 🛣️ Registra rotas e middlewares personalizados
registrar_rotas(app)
register_error_handlers(app)

# 📂 Endpoint para servir arquivos estáticos
@app.route("/uploads/<path:filename>")
def servir_arquivo_estatico(filename):
    return send_from_directory("uploads", filename)

# 🌱 Rota principal
@app.route("/")
def home():
    return "AMS - Agro Marketing Service - Plataforma de intermediação entre fazendeiros e prestadores de serviço"

# ▶️ Executa o servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
