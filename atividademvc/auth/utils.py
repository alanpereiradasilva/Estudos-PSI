from extensions import login_manager
from models import User

@login_manager.user_loader
def load_user(user_id):
    """
    Função do Flask-Login para carregar um usuário pelo seu ID.
    O ID é armazenado na sessão.
    """
    if user_id is not None:
        return User.query.get(int(user_id))
    return None