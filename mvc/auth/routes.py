# routes.py (Para centralizar o registro dos Blueprints)
from controllers.auth_controller import auth_bp
from controllers.produto_controller import produtos_bp

def init_app(app):
    """
    Função para registrar todos os Blueprints na aplicação.
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(produtos_bp)