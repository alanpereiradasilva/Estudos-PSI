import os
from flask import Flask, url_for, redirect


from config import Config
from extensions import init_extensions, db, login_manager


from models import * 
from auth.routes import auth_bp
from controllers.user_controller import user_bp
from controllers.product_controller import product_bp


def create_app(config_class=Config):
    """Função factory para criar a instância da aplicação."""
    app = Flask(__name__)
    app.config.from_object(config_class)


    init_extensions(app)


    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    
    
    @app.route('/')
    def index():
        
        return redirect(url_for('product.list_products'))

    
    @app.shell_context_processor
    def make_shell_context():
        
        return {'db': db, 'User': User, 'Product': Product}

    return app


app = create_app()


with app.app_context():

    db.create_all()