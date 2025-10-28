from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from modelos import User, session 


# Alterado de 'users_bp' para 'auth_bp'
auth_bp = Blueprint('auth', __name__, url_prefix='/auth') 

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        email = request.form['email'].strip()
        password = request.form['senha'].strip()

        with session.begin():
            if session.execute(select(User).where(User.email == email)).scalar_one_or_none():
                flash('Email já está em uso.', 'warning')
                return render_template('auth/register.html')
            
            hashed_password = generate_password_hash(password, method='scrypt')
            new_user = User(username=nome, email=email, password_hash=hashed_password)
            session.add(new_user)
            flash('Conta criada com sucesso! Faça login.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html') 


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['senha'].strip()

        with session.begin():
            user = session.execute(select(User).where(User.email == email)).scalar_one_or_none()
            session.expunge_all() 

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Email ou senha inválidos.', 'danger')

    return render_template('auth/login.html') 

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', user=current_user) 

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('index'))