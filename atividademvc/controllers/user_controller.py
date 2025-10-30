from flask import Blueprint, render_template
from flask_login import login_required, current_user

user_bp = Blueprint('user', __name__, url_prefix='/user', template_folder='templates')

@user_bp.route('/profile')
@login_required 
def profile():
    """Exibe a página de perfil do usuário logado."""

    return render_template('users/profile.html', user=current_user)

