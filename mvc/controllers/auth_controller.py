from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from modelos import Produto, session, User
from sqlalchemy import select, desc
from sqlalchemy.exc import IntegrityError
from datetime import datetime 


produtos_bp = Blueprint('produtos', __name__, url_prefix='/produtos')


@produtos_bp.route('/', methods=['GET'])
@login_required
def listar_produtos():
    """Lista todos os produtos do usuário logado."""
    with session.begin():
        stmt = select(Produto).where(Produto.user_id == current_user.id).order_by(desc(Produto.id))
        produtos = session.execute(stmt).scalars().all()
        session.expunge_all() # Desanexa os objetos para evitar problemas de sessão

    return render_template('produtos/lista.html', produtos=produtos)



@produtos_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def adicionar_produto():
    if request.method == 'POST':
        name = request.form['name'].strip()
        description = request.form['description'].strip()
        price_str = request.form['price'].strip().replace(',', '.') #Substitui vírgula por ponto, Gustavo Guanabara ensinou

        try:
            price = float(price_str)
            
            novo_produto = Produto(
                name=name,
                description=description,
                price=price,
                user_id=current_user.id 
            )

            with session.begin():
                session.add(novo_produto)
            
            flash('Produto adicionado com sucesso!', 'success')
            return redirect(url_for('produtos.listar_produtos'))

        except ValueError:
            flash('Preço inválido. Certifique-se de que é um número.', 'danger')
        except IntegrityError:
            flash('Erro ao adicionar produto: Falha de integridade dos dados.', 'danger')
        except Exception as e:
            flash(f'Erro desconhecido ao adicionar produto: {e}', 'danger')
            
    return render_template('produtos/novo.html')



@produtos_bp.route('/editar/<int:produto_id>', methods=['GET', 'POST'])
@login_required
def editar_produto(produto_id):
    with session.begin():
        produto = session.get(Produto, produto_id)
        if not produto or produto.user_id != current_user.id:
            session.expunge_all()
            flash('Produto não encontrado ou você não tem permissão para editá-lo.', 'danger')
            return redirect(url_for('produtos.listar_produtos'))
            
        if request.method == 'POST':
            name = request.form['name'].strip()
            description = request.form['description'].strip()
            price_str = request.form['price'].strip().replace(',', '.')
            
            try:
                price = float(price_str)

                produto.name = name
                produto.description = description
                produto.price = price
                
                
                session.expunge(produto) # Desanexa para o objeto não ser mais associado a esta sessão
                flash('Produto atualizado com sucesso!', 'success')
                return redirect(url_for('produtos.listar_produtos'))
            
            except ValueError:
                flash('Preço inválido. Certifique-se de que é um número.', 'danger')
                session.expunge(produto) # Desanexa o objeto para evitar que o erro da sessão persista
            except Exception as e:
                flash(f'Erro ao atualizar produto: {e}', 'danger')
                session.expunge(produto)

        else: 
            session.expunge(produto)
            return render_template('produtos/editar.html', produto=produto)
            

    return redirect(url_for('produtos.listar_produtos'))



@produtos_bp.route('/excluir/<int:produto_id>', methods=['POST'])
@login_required
def excluir_produto(produto_id):
    with session.begin():
        produto = session.get(Produto, produto_id)

        if not produto or produto.user_id != current_user.id:
            session.expunge_all()
            flash('Produto não encontrado ou você não tem permissão para excluí-lo.', 'danger')
            return redirect(url_for('produtos.listar_produtos'))

        try:
            session.delete(produto)
            
            flash('Produto excluído com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao excluir produto: {e}', 'danger')
            
    return redirect(url_for('produtos.listar_produtos'))