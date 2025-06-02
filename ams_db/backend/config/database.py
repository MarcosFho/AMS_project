import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

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
