from backend.models.cliente_model import Cliente
from backend.config.session import get_db

# 🔹 Criar um novo cliente
def criar_cliente(dados_cliente):
    with get_db() as db:
        cliente = Cliente(**dados_cliente)
        db.add(cliente)
        db.commit()               # ✅ necessário para persistir no banco
        db.refresh(cliente)
        return cliente

# 🔹 Listar todos os clientes
def listar_clientes():
    with get_db() as db:
        return db.query(Cliente).all()

# 🔹 Buscar cliente pelo ID
def buscar_cliente(id):
    with get_db() as db:
        return db.query(Cliente).filter(Cliente.id == id).first()

# 🔹 Atualizar um cliente
def atualizar_cliente(id, dados_cliente):
    with get_db() as db:
        cliente = db.query(Cliente).filter(Cliente.id == id).first()
        if cliente:
            for key, value in dados_cliente.items():
                setattr(cliente, key, value)
            db.commit()           # ✅ necessário após atualizar
            db.refresh(cliente)
        return cliente

# 🔹 Deletar cliente
def deletar_cliente(id):
    with get_db() as db:
        cliente = db.query(Cliente).filter(Cliente.id == id).first()
        if cliente:
            db.delete(cliente)
            db.commit()           # ✅ necessário após deletar
        return cliente

# 🔹 Buscar cliente pelo ID de usuário
def buscar_cliente_por_usuario(id_usuario):
    with get_db() as db:
        return db.query(Cliente).filter(Cliente.id_usuario == id_usuario).first()
