from flask import render_template
from flask_login import current_user

def list_products(products):
    return render_template(
        "baby_products.html",
        products=products,
        title="Lista de productos",
        current_user=current_user,
    )

def create_product():
    return render_template(
        "create_products.html", title="Crear Producto", current_user=current_user
    )

def update_product(product):
    return render_template(
        "update_products.html",
        title="Editar Producto",
        product=product,
        current_user=current_user,
    )