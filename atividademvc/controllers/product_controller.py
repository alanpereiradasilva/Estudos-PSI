from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.product import Product
from extensions import db

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
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        
        
        new_product = Product(
            name=name, 
            description=description, 
            price=float(price),
            owner=current_user 
        )
        db.session.add(new_product)
        db.session.commit()
        flash(f'Produto "{name}" adicionado com sucesso!', 'success')
        return redirect(url_for('product.list_products'))
        
    return render_template('products/add.html')
    
# Implementações de Edit e Delete seriam similares