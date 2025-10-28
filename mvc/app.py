# app.py
from flask import Flask, render_template
from flask_login import LoginManager
from models import User, session, Base, engine
from routes import init_app # Importa a função de registro de rotas
from controllers.auth_controller import auth_bp
from controllers.produto_controller import produtos_bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'segredo123'

    
    login_manager = LoginManager()

    app.register_blueprint(auth_bp)
    app.register_blueprint(produtos_bp)
    
    # Ajuste o login_view para o novo nome do Blueprint
    login_manager.login_view = 'auth.login' 
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        with session.begin():
            # Uso de session.get é mais direto para buscar por primary key
            user_data = session.get(User, user_id) 
            session.expunge_all() 
        return user_data

    
    # Registro dos Blueprints usando o routes.py
    init_app(app)

    
    @app.route('/')
    def index():
        return render_template('index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)