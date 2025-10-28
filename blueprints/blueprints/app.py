from flask import Flask, render_template
from flask_login import LoginManager
from models import User, session, Base, engine


from blueprints.users import users_bp
from blueprints.livros import livros_bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'segredo123'

    
    login_manager = LoginManager()
    
    login_manager.login_view = 'users.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        with session.begin():
            user_data = session.query(User).where(User.id == user_id).first()
            session.expunge_all() 
            session.close()
        return user_data

    
    app.register_blueprint(users_bp)
    app.register_blueprint(livros_bp)

    
    @app.route('/')
    def index():
        return render_template('index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)