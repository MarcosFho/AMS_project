import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from config.session import get_db
from models.usuario_model import Usuario
from models.tipo_usuario_model import TipoUsuario
from models.login_model import Login
from utils.crypto import gerar_hash_senha
from sqlalchemy.exc import IntegrityError

# 🔹 0. Popular tipos de usuário
def popular_tipos_usuario():
    tipos = ["CLIENTE", "PRESTADOR", "LOJA", "USUARIO", "ADMIN"]

    with get_db() as db:
        for nome in tipos:
            if db.query(TipoUsuario).filter_by(nome=nome).first():
                continue
            tipo = TipoUsuario(nome=nome)
            db.add(tipo)

        try:
            db.commit()
            print("Tipos de usuário inseridos com sucesso!")
        except IntegrityError as e:
            db.rollback()
            print("Erro ao inserir tipos de usuário:", e)

# 🔹 1. Popular usuários
def popular_usuarios():
    usuarios = [
        {"nome": "João da Roça", "email": "joao@roca.com", "telefone": "34991234567", "tipo_usuario": "PRESTADOR"},
        {"nome": "Maria Produtora", "email": "maria@fazenda.com", "telefone": "31998765432", "tipo_usuario": "CLIENTE"},
        {"nome": "Carlos AgroTech", "email": "carlos@agro.com", "telefone": "35998876655", "tipo_usuario": "PRESTADOR"},
        {"nome": "Ana Sementes", "email": "ana@sementes.com", "telefone": "62996667788", "tipo_usuario": "CLIENTE"},
            {
        "nome": "Loja do Campo",
        "email": "contato@lojacampo.com",
        "telefone": "3499887766",
        "tipo_usuario": "LOJA",
        "foto_url": "https://img.icons8.com/ios/452/shop.png"
    },
    {
        "nome": "AgroMais",
        "email": "vendas@agromais.com",
        "telefone": "3499111222",
        "tipo_usuario": "LOJA",
        "foto_url": "https://img.icons8.com/ios/452/tractor.png"
    },

    ]

    senha_padrao = gerar_hash_senha("123456")

    with get_db() as db:
        for dados in usuarios:
            tipo = db.query(TipoUsuario).filter(TipoUsuario.nome == dados["tipo_usuario"]).first()
            if not tipo:
                print(f"Tipo de usuário {dados['tipo_usuario']} não encontrado. Pulei.")
                continue

            if db.query(Usuario).filter(Usuario.email == dados["email"]).first():
                print(f"Usuário {dados['email']} já existe. Pulei.")
                continue

            usuario = Usuario(
                nome=dados["nome"],
                email=dados["email"],
                telefone=dados["telefone"],
                tipo_usuario_id=tipo.id
            )
            db.add(usuario)
            db.flush()

            login = Login(
                id_usuario=usuario.id,
                senha_hash=senha_padrao,
                ativo=1
            )
            db.add(login)

        try:
            db.commit()
            print("Usuários inseridos com sucesso!")
        except IntegrityError as e:
            db.rollback()
            print("Erro de integridade:", e)

# 🔹 1.1 Popular prestadores
def popular_prestadores():
    from models.prestador_model import Prestador
    from models.usuario_model import Usuario
    from models.tipo_usuario_model import TipoUsuario
    from config.session import get_db
    from sqlalchemy.exc import IntegrityError

    prestadores_dados = [
        {
            "localizacao": "Uberlândia - MG",
            "avaliacao_media": 4.5,
            "categoria": "AGRONOMICO",
        },
        {
            "localizacao": "Patos de Minas - MG",
            "avaliacao_media": 4.8,
            "categoria": "VETERINARIO",
        },
    ]

    with get_db() as db:
        tipo_prestador = db.query(TipoUsuario).filter_by(nome="PRESTADOR").first()
        if not tipo_prestador:
            print("Tipo PRESTADOR não encontrado. Pulei prestadores.")
            return

        usuarios = db.query(Usuario).filter_by(tipo_usuario_id=tipo_prestador.id).all()
        if not usuarios:
            print("Nenhum usuário do tipo PRESTADOR encontrado.")
            return

        for idx, usuario in enumerate(usuarios):
            if db.query(Prestador).filter_by(id_usuario=usuario.id).first():
                print(f"Prestador com id_usuario {usuario.id} já existe. Pulei.")
                continue

            dados = prestadores_dados[idx % len(prestadores_dados)]
            prestador = Prestador(
                id_usuario=usuario.id,
                localizacao=dados["localizacao"],
                avaliacao_media=dados["avaliacao_media"],
                categoria=dados["categoria"]
            )
            db.add(prestador)

        try:
            db.commit()
            print("Prestadores inseridos com sucesso!")
        except IntegrityError as e:
            db.rollback()
            print("Erro ao inserir prestadores:", e)

# 🔹 2. Popular lojas
def popular_lojas():
    from models.loja_model import Loja
    from models.endereco_model import Endereco
    from models.tipo_usuario_model import TipoUsuario
    from models.usuario_model import Usuario

    from config.session import get_db

    with get_db() as db:
        usuarios_loja = db.query(Usuario).join(TipoUsuario).filter(
        TipoUsuario.nome == "LOJA"
        ).all()

        if not usuarios_loja:
            print("Nenhum usuário do tipo LOJA encontrado. Pulei lojas.")
            return

        lojas = [
            {
                "nome": "AgroCenter",
                "razao_social": "AgroCenter LTDA",
                "cnpj": "12.345.678/0001-99",
                "telefone": "3499001122",
            },
            {
                "nome": "FazendaStore",
                "razao_social": "Fazenda Store Comercial Rural",
                "cnpj": "98.765.432/0001-55",
                "telefone": "31988776655",
            },
        ]

        for dados_loja, usuario in zip(lojas, usuarios_loja):
            if db.query(Loja).filter(Loja.nome == dados_loja["nome"]).first():
                print(f"Loja {dados_loja['nome']} já existe. Pulei.")
                continue

        endereco = Endereco(
            rua="Rua Principal",
            numero="100",
            bairro="Centro",
            cidade="Uberlândia",
            estado="MG",
            cep="38400-000"
        )
        db.add(endereco)
        db.flush()

        loja = Loja(
            id_usuario=usuario.id,
            nome=dados_loja["nome"],
            razao_social=dados_loja["razao_social"],
            cnpj=dados_loja["cnpj"],
            telefone=dados_loja["telefone"],
            id_endereco=endereco.id
        )
        db.add(loja)

        try:
            db.commit()
            print("Lojas inseridas com sucesso!")
        except Exception as e:
            db.rollback()
            print("Erro ao inserir lojas:", e)

# 🔹 3. Popular serviços
def popular_servicos():
    from models.servico_model import Servico
    from models.prestador_model import Prestador
    from datetime import datetime

    servicos = [
        {
            "nome": "Consulta Agronômica",
            "descricao": "Análise de solo, plantio e adubação para produtores rurais.",
            "categoria": "AGRONOMICO",
            "preco": 150.00,
        },
        {
            "nome": "Vacinação de Bovinos",
            "descricao": "Aplicação de vacinas para gado de corte e leite.",
            "categoria": "VETERINARIO",
            "preco": 80.00,
        },
        {
            "nome": "Aplicação de Defensivos",
            "descricao": "Aplicação segura e controlada com drone agrícola.",
            "categoria": "AGRONOMICO",
            "preco": 200.00,
        },
        {
            "nome": "Manutenção de Tratores",
            "descricao": "Revisão e conserto de tratores agrícolas.",
            "categoria": "TECNICO",
            "preco": 250.00,
        },
        {
            "nome": "Elaboração de Projetos Técnicos",
            "descricao": "Projetos para obtenção de crédito e licenciamento.",
            "categoria": "PROJETOS",
            "preco": 300.00,
        },
    ]

    with get_db() as db:
        prestadores = db.query(Prestador).all()
        if not prestadores:
            print("Nenhum prestador encontrado. Pulei serviços.")
            return

        for idx, dados in enumerate(servicos):
            if db.query(Servico).filter(Servico.nome == dados["nome"]).first():
                print(f"Serviço '{dados['nome']}' já existe. Pulei.")
                continue

            prestador = prestadores[idx % len(prestadores)]  # distribui entre os existentes

            servico = Servico(
                nome=dados["nome"],
                descricao=dados["descricao"],
                categoria=dados["categoria"],
                preco=dados["preco"],
                id_prestador=prestador.id,
                data_cadastro=datetime.utcnow()
            )
            db.add(servico)

        try:
            db.commit()
            print("Serviços inseridos com sucesso!")
        except IntegrityError as e:
            db.rollback()
            print("Erro ao inserir serviços:", e)

# 🔹 4. Popular produtos
def popular_produtos():
    from models.produto_model import Produto
    from models.loja_model import Loja
    from datetime import datetime

    produtos = [
        {
            "nome": "Adubo Orgânico Premium",
            "descricao": "Ideal para hortas e lavouras com alta produtividade.",
            "preco": 85.50,
            "quantidade_estoque": 100,
            "categoria": "Fertilizantes"
        },
        {
            "nome": "Semente de Milho Híbrido",
            "descricao": "Alta resistência e produtividade para safra longa.",
            "preco": 190.00,
            "quantidade_estoque": 200,
            "categoria": "Sementes"
        },
        {
            "nome": "Trator Massey 275",
            "descricao": "Trator seminovo, revisado, excelente para pequenas propriedades.",
            "preco": 95000.00,
            "quantidade_estoque": 2,
            "categoria": "Máquinas"
        },
        {
            "nome": "Herbicida Seletivo",
            "descricao": "Controle eficaz de ervas daninhas sem prejudicar a lavoura.",
            "preco": 120.00,
            "quantidade_estoque": 75,
            "categoria": "Insumos"
        },
        {
            "nome": "Ração Proteica para Gado",
            "descricao": "Suplemento alimentar para bovinos de corte e leite.",
            "preco": 140.00,
            "quantidade_estoque": 60,
            "categoria": "Nutrição Animal"
        },
        {
            "nome": "Bebedouro Automático para Suínos",
            "descricao": "Equipamento resistente e higiênico para alimentação animal.",
            "preco": 220.00,
            "quantidade_estoque": 20,
            "categoria": "Equipamentos"
        },
        {
            "nome": "Vacina contra Aftosa",
            "descricao": "Proteção essencial para bovinos e bubalinos.",
            "preco": 35.00,
            "quantidade_estoque": 120,
            "categoria": "Medicamentos"
        },
        {
            "nome": "Touca para Ordenha",
            "descricao": "Utensílio de higiene para uso durante a ordenha.",
            "preco": 9.90,
            "quantidade_estoque": 300,
            "categoria": "Utensílios"
        },
        {
            "nome": "Sal Mineral para Gado",
            "descricao": "Produto mineralizado para suplementação bovina.",
            "preco": 75.00,
            "quantidade_estoque": 150,
            "categoria": "Agropecuária"
        }
    ]

    with get_db() as db:
        lojas = db.query(Loja).all()
        if not lojas:
            print("Nenhuma loja encontrada. Pulei produtos.")
            return

        for idx, dados in enumerate(produtos):
            if db.query(Produto).filter(Produto.nome == dados["nome"]).first():
                print(f"Produto '{dados['nome']}' já existe. Pulei.")
                continue

            loja = lojas[idx % len(lojas)]

            produto = Produto(
                nome=dados["nome"],
                descricao=dados["descricao"],
                preco=dados["preco"],
                quantidade_estoque=dados["quantidade_estoque"],
                categoria=dados["categoria"],
                id_loja=loja.id,
                data_cadastro=datetime.utcnow()
            )
            db.add(produto)

        try:
            db.commit()
            print("Produtos inseridos com sucesso!")
        except IntegrityError as e:
            db.rollback()
            print("Erro ao inserir produtos:", e)

# 🔹 5. Popular cupons promocionais
def popular_cupons():
    from models.cupom_model import CupomPromocional
    from datetime import datetime, timedelta

    cupons = [
        {
            "codigo": "DESCONTO10",
            "descricao": "Cupom de 10% para novos clientes",
            "desconto_percentual": 10.0,
            "data_expiracao": datetime.utcnow() + timedelta(days=15)
        },
        {
            "codigo": "BOASVINDAS20",
            "descricao": "Desconto especial de boas-vindas",
            "desconto_percentual": 20.0,
            "data_expiracao": datetime.utcnow() + timedelta(days=30)
        },
        {
            "codigo": "FRETEGRATIS",
            "descricao": "Frete grátis em compras acima de R$ 300",
            "desconto_percentual": 0.0,
            "data_expiracao": datetime.utcnow() + timedelta(days=10)
        },
    ]

    with get_db() as db:
        for dados in cupons:
            if db.query(CupomPromocional).filter(CupomPromocional.codigo == dados["codigo"]).first():
                print(f"Cupom '{dados['codigo']}' já existe. Pulei.")
                continue

            cupom = CupomPromocional(**dados)
            db.add(cupom)

        try:
            db.commit()
            print("Cupons inseridos com sucesso!")
        except IntegrityError as e:
            db.rollback()
            print("Erro ao inserir cupons:", e)

if __name__ == "__main__":
    popular_tipos_usuario()
    popular_usuarios()
    popular_prestadores()
    popular_lojas()
    popular_servicos()
    popular_produtos()
    popular_cupons()