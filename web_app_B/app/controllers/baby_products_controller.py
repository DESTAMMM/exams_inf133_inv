from flask import Blueprint, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.baby_products_model import Product  
from views import baby_products_view  
from utils.decorators import role_required

product_bp = Blueprint("product", __name__)

@product_bp.route("/products")
@login_required
def list_products():
    products = Product.get_all()
    return baby_products_view.list_products(products)

@product_bp.route("/products/create", methods=["GET", "POST"])
@login_required
@role_required("admin")
def create_product():
    if request.method == "POST":
        if current_user.has_role("admin"):
            nombre = request.form["nombre"]
            tipo = request.form["tipo"]
            marca = request.form["marca"]
            precio = float(request.form["precio"])
            cantidad = int(request.form["cantidad"])
            proveedor = request.form["proveedor"]
            codigo_barra = request.form["codigo_barra"]
            
            product = Product(
                nombre=nombre,
                tipo=tipo,
                marca=marca,
                precio=precio,
                cantidad=cantidad,
                proveedor=proveedor,
                codigo_barra=codigo_barra
            )
            product.save()
            flash("Producto creado exitosamente", "success")
            return redirect(url_for("product.list_products"))
        else:
            return jsonify({"message": "Unauthorized"}), 403
    return baby_products_view.create_product()

@product_bp.route("/products/<int:id>/update", methods=["GET", "POST"])
@login_required
@role_required("admin")
def update_product(id):
    product = Product.get_by_id(id)
    if not product:
        return "Producto no encontrado", 404
    if request.method == "POST":
        if current_user.has_role("admin"):
            product.nombre = request.form["nombre"]
            product.tipo = request.form["tipo"]
            product.marca = request.form["marca"]
            product.precio = float(request.form["precio"])
            product.cantidad = int(request.form["cantidad"])
            product.proveedor = request.form["proveedor"]
            product.codigo_barra = request.form["codigo_barra"]
            product.update()
            flash("Producto actualizado exitosamente", "success")
            return redirect(url_for("product.list_products"))
        else:
            return jsonify({"message": "Unauthorized"}), 403
    return baby_products_view.update_product(product)

@product_bp.route("/products/<int:id>/delete")
@login_required
@role_required("admin")
def delete_product(id):
    product = Product.get_by_id(id)
    if not product:
        return "Producto no encontrado", 404
    if current_user.has_role("admin"):
        product.delete()
        flash("Producto eliminado exitosamente", "success")
        return redirect(url_for("product.list_products"))
    else:
        return jsonify({"message": "Unauthorized"}), 403