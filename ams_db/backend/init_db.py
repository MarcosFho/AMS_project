import sys
import os

# Garante que o caminho do projeto seja reconhecido no ambiente local
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.config.database import Base, engine
from backend.config.session import SessionLocal
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# ✅ Importações obrigatórias para registrar os modelos
# (Esses devem vir ANTES do create_all)
import backend.models.tipo_usuario_model
import backend.models.usuario_model
import backend.models.login_model
import backend.models.endereco_model
import backend.models.cliente_model
import backend.models.prestador_model
import backend.models.fazenda_model
import backend.models.fazenda_foto_model
import backend.models.loja_model
import backend.models.produto_model
import backend.models.produto_foto_model
import backend.models.servico_model
import backend.models.servico_foto_model
import backend.models.avaliacao_model
import backend.models.mensagem_model
import backend.models.fale_conosco_model
import backend.models.trabalhe_conosco_model
import backend.models.pessoa_fisica_model
import backend.models.pessoa_juridica_model
import backend.models.solicitacao_model

# ✅ Criação das tabelas
print("📦 Criando/atualizando todas as tabelas...")
try:
    Base.metadata.create_all(engine)
    print("✅ Tabelas criadas com sucesso.")
except SQLAlchemyError as e:
    print("❌ Falha ao criar tabelas:", e)
    sys.exit(1)

# ✅ Validação da existência da tabela tipo_usuario
db = SessionLocal()
try:
    print("🔎 Verificando existência da tabela tipo_usuario...")
    db.execute(text("SELECT 1 FROM tipo_usuario LIMIT 1;"))
    print("✅ A tabela tipo_usuario existe.")
except Exception as e:
    print("❌ A tabela tipo_usuario NÃO foi criada corretamente.")
    print("Erro:", e)
    db.rollback()
    db.close()
    sys.exit(1)

# ✅ Inserção dos tipos de usuário
print("🧩 Inserindo tipos de usuário padrão...")
from backend.models.tipo_usuario_model import TipoUsuario

tipos = ['CLIENTE', 'PRESTADOR', 'LOJA', 'USUARIO', 'ADMIN']

try:
    for nome in tipos:
        if not db.query(TipoUsuario).filter_by(nome=nome).first():
            db.add(TipoUsuario(nome=nome))
    db.commit()
    print("✅ Tipos de usuário inseridos com sucesso.")
except SQLAlchemyError as e:
    print("❌ Erro ao inserir tipos de usuário:", e)
    db.rollback()
finally:
    db.close()

# ✅ Listagem final das tabelas
print("\n📄 Tabelas registradas:")
for table_name in Base.metadata.tables:
    print(f" - {table_name}")

print("\n🚀 Banco inicializado com sucesso.")
