from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Livro, session 
from sqlalchemy import select


livros_bp = Blueprint('livros', __name__, url_prefix='/livros')


@livros_bp.route('/')
@login_required
def listar_livros():
    with session.begin():
        
        stmt = select(Livro).where(Livro.autor_id == current_user.id)
        livros = session.execute(stmt).scalars().all()
        session.close()

    return render_template('livros.html', livros=livros)


@livros_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        ano = request.form['ano']

        with session.begin():
            livro = Livro(titulo=titulo, ano=int(ano), autor_id=current_user.id)
            session.add(livro)
            flash('Livro adicionado com sucesso!', 'success')
            return redirect(url_for('livros.listar_livros')) 

    return render_template('livro_form.html', action='Adicionar')


@livros_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_livro(id):
    with session.begin():
        livro = session.query(Livro).where(Livro.id == id, Livro.autor_id == current_user.id).first()

        if not livro:
            flash('Livro não encontrado ou você não tem permissão.', 'danger')
            return redirect(url_for('livros.listar_livros'))

        if request.method == 'POST':
            livro.titulo = request.form['titulo']
            livro.ano = request.form['ano']
            flash('Livro atualizado com sucesso!', 'success')
            return redirect(url_for('livros.listar_livros'))

        
        session.expunge(livro)
        session.close()

    return render_template('livro_form.html', action='Editar', livro=livro)


@livros_bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_livro(id):
    with session.begin():
        livro = session.query(Livro).where(Livro.id == id, Livro.autor_id == current_user.id).first()

        if livro:
            session.delete(livro)
            flash('Livro excluído com sucesso!', 'success')
        else:
            flash('Livro não encontrado ou você não tem permissão para excluir.', 'danger')

    return redirect(url_for('livros.listar_livros'))