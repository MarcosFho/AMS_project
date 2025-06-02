import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# Ajusta o caminho para encontrar o arquivo .env na raiz do projeto
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
env_path = os.path.join(root_dir, ".env")

# Carrega variáveis do .env
load_dotenv(env_path)

# Lê as variáveis de ambiente
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Monta a URL de conexão
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Cria o engine SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
Base = declarative_base()

def init_db():
    """Inicializa o banco de dados criando todas as tabelas"""
    # Importa os modelos individualmente para evitar o wildcard import
    from backend.models.usuario_model import Usuario
    from backend.models.tipo_usuario_model import TipoUsuario
    from backend.models.pessoa_fisica_model import PessoaFisica
    from backend.models.pessoa_juridica_model import PessoaJuridica
    from backend.models.endereco_model import Endereco
    from backend.models.login_model import Login
    from backend.models.produto_model import Produto
    from backend.models.servico_model import Servico
    from backend.models.avaliacao_model import Avaliacao
    from backend.models.mensagem_model import Mensagem
    from backend.models.solicitacao_model import Solicitacao
    from backend.models.fazenda_model import Fazenda
    
    Base.metadata.create_all(bind=engine)
