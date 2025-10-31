from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models.product import Product
from extensions import db
from forms import ProductForm # Importado no passo anterior

product_bp = Blueprint('product', __name__, url_prefix='/products', template_folder='templates')

@product_bp.route('/')
@login_required 
def list_products():
    """Lista todos os produtos do usuário logado."""
    products = current_user.products.all()
    return render_template('products/list.html', products=products)

@product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm() 
    
    if form.validate_on_submit(): 
        name = form.name.data
        description = form.description.data
        price = form.price.data
        
        new_product = Product(
            name=name, 
            description=description, 
            price=price,
            owner=current_user 
        )
        db.session.add(new_product)
        db.session.commit()
        flash(f'Produto "{name}" adicionado com sucesso!', 'success')
        return redirect(url_for('product.list_products'))
        
    return render_template('products/add.html', form=form)


@product_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    """Edita um produto existente, se pertencer ao usuário logado."""
    product = Product.query.get_or_404(product_id)
    
    # Verificação de Autorização: Apenas o dono pode editar
    if product.owner != current_user:
        flash('Você não tem permissão para editar este produto.', 'danger')
        return redirect(url_for('product.list_products'))
        
    form = ProductForm(obj=product) # Preenche o formulário com os dados do produto (GET)
    
    if form.validate_on_submit():
        # Atualiza os dados do objeto Product com os dados do formulário
        form.populate_obj(product) 
        db.session.commit()
        flash(f'Produto "{product.name}" atualizado com sucesso!', 'success')
        return redirect(url_for('product.list_products'))
        
    return render_template('products/edit.html', form=form, product_id=product.id)


@product_bp.route('/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    """Exclui um produto existente, se pertencer ao usuário logado."""
    product = Product.query.get_or_404(product_id)
    
    # Verificação de Autorização: Apenas o dono pode excluir
    if product.owner != current_user:
        flash('Você não tem permissão para excluir este produto.', 'danger')
        return redirect(url_for('product.list_products'))
        
    db.session.delete(product)
    db.session.commit()
    flash(f'Produto "{product.name}" excluído com sucesso!', 'success')
    return redirect(url_for('product.list_products'))

# Implementações de Edit e Delete seriam similares