from flask import Blueprint, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.bath_products_model import ProductosDeBano
from views import bath_products_view
from utils.decorators import role_required

bath_product_bp = Blueprint("bath_product", __name__)

@bath_product_bp.route("/bath_products")
@login_required
def list_products():
    products = ProductosDeBano.get_all()
    return bath_products_view.list_products(products)

@bath_product_bp.route("/bath_products/create", methods=["GET", "POST"])
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
            material = request.form["material"]
            color = request.form["color"]
            peso = float(request.form["peso"])
            dimensiones = request.form["dimensiones"]
            descripcion = request.form["descripcion"]
            uso = request.form["uso"]
            seguridad = request.form["seguridad"]
            stock = int(request.form["stock"])
            
            product = ProductosDeBano(
                nombre=nombre,
                tipo=tipo,
                marca=marca,
                precio=precio,
                cantidad=cantidad,
                proveedor=proveedor,
                codigo_barra=codigo_barra,
                material=material,
                color=color,
                peso=peso,
                dimensiones=dimensiones,
                descripcion=descripcion,
                uso=uso,
                seguridad=seguridad,
                stock=stock
            )
            product.save()
            flash("Producto creado exitosamente", "success")
            return redirect(url_for("bath_product.list_products"))
        else:
            return jsonify({"message": "Unauthorized"}), 403
    return bath_products_view.create_product()

@bath_product_bp.route("/bath_products/<int:id>/update", methods=["GET", "POST"])
@login_required
@role_required("admin")
def update_product(id):
    product = ProductosDeBano.get_by_id(id)
    if not product:
        return "Producto no encontrado", 404
    if request.method == "POST":
        if current_user.has_role("admin"):
            product.pbano_nombre = request.form["nombre"]
            product.pbano_tipo = request.form["tipo"]
            product.pbano_marca = request.form["marca"]
            product.pbano_precio = float(request.form["precio"])
            product.pbano_cantidad = int(request.form["cantidad"])
            product.pbano_proveedor = request.form["proveedor"]
            product.pbano_codigo_barra = request.form["codigo_barra"]
            product.pbano_material = request.form["material"]
            product.pbano_color = request.form["color"]
            product.pbano_peso = float(request.form["peso"])
            product.pbano_dimensiones = request.form["dimensiones"]
            product.pbano_descripcion = request.form["descripcion"]
            product.pbano_uso = request.form["uso"]
            product.pbano_seguridad = request.form["seguridad"]
            product.pbano_stock = int(request.form["stock"])
            
            product.update()
            flash("Producto actualizado exitosamente", "success")
            return redirect(url_for("bath_product.list_products"))
        else:
            return jsonify({"message": "Unauthorized"}), 403
    return bath_products_view.update_product(product)

@bath_product_bp.route("/bath_products/<int:id>/delete")
@login_required
@role_required("admin")
def delete_product(id):
    product = ProductosDeBano.get_by_id(id)
    if not product:
        return "Producto no encontrado", 404
    if current_user.has_role("admin"):
        product.delete()
        flash("Producto eliminado exitosamente", "success")
        return redirect(url_for("bath_product.list_products"))
    else:
        return jsonify({"message": "Unauthorized"}), 403