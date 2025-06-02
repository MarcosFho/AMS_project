from flask import Flask
from backend.controllers.avaliacao_controller import avaliacao_bp
from backend.controllers.cliente_controller import cliente_bp
from backend.controllers.produto_controller import produto_bp
from backend.controllers.servico_controller import servico_bp
from backend.controllers.prestador_controller import prestador_bp
from backend.controllers.endereco_controller import endereco_bp
from backend.controllers.loja_controller import loja_bp
from backend.controllers.login_controller import login_bp
from backend.controllers.pessoa_fisica_controller import pessoa_fisica_bp
from backend.controllers.pessoa_juridica_controller import pessoa_juridica_bp
from backend.controllers.fale_conosco_controller import fale_conosco_bp
from backend.controllers.trabalhe_conosco_controller import trabalhe_conosco_bp
from backend.controllers.fazenda_controller import fazenda_bp
from backend.controllers.fazenda_foto_controller import fazenda_foto_bp
from backend.controllers.produto_foto_controller import produto_foto_bp
from backend.controllers.servico_foto_controller import servico_foto_bp
from backend.controllers.solicitacao_controller import solicitacao_bp
from backend.controllers.mensagem_controller import mensagem_bp
from backend.controllers.usuario_controller import usuario_bp
from backend.controllers.health_controller import health_bp
from backend.controllers.tipo_usuario_controller import tipo_usuario_bp

def registrar_rotas(app: Flask):
    app.register_blueprint(avaliacao_bp, url_prefix="/api")
    app.register_blueprint(cliente_bp, url_prefix="/api")
    app.register_blueprint(produto_bp, url_prefix="/api")
    app.register_blueprint(servico_bp, url_prefix="/api")
    app.register_blueprint(prestador_bp, url_prefix="/api")
    app.register_blueprint(endereco_bp, url_prefix="/api")
    app.register_blueprint(loja_bp, url_prefix="/api")
    app.register_blueprint(login_bp, url_prefix="/api")
    app.register_blueprint(pessoa_fisica_bp, url_prefix="/api")
    app.register_blueprint(pessoa_juridica_bp, url_prefix="/api")
    app.register_blueprint(fale_conosco_bp, url_prefix="/api")
    app.register_blueprint(trabalhe_conosco_bp, url_prefix="/api")
    app.register_blueprint(fazenda_bp, url_prefix="/api")
    app.register_blueprint(fazenda_foto_bp, url_prefix="/api")
    app.register_blueprint(produto_foto_bp, url_prefix="/api")
    app.register_blueprint(servico_foto_bp, url_prefix="/api")
    app.register_blueprint(solicitacao_bp, url_prefix="/api")
    app.register_blueprint(mensagem_bp, url_prefix="/api")
    app.register_blueprint(usuario_bp, url_prefix="/api")
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(tipo_usuario_bp, url_prefix="/api")
