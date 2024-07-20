from flask import Blueprint, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from models.bath_products_model import ProductosDeBano
from views import bath_products_view
from utils.decorators import role_required
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
    
@bath_product_bp.route("/bath_products/download_pdf")
@login_required
@role_required("admin")
def download_pdf():
    # Crear un buffer en memoria para el PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Añadir título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "Lista de Productos de Baño")

    # Configurar el font
    c.setFont("Helvetica", 12)

    # Obtener todos los productos
    products = ProductosDeBano.get_all()

    # Añadir productos al PDF
    y_position = height - 100
    for product in products:
        if y_position < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 50
        c.drawString(100, y_position, f"Nombre: {product.pbano_nombre}")
        c.drawString(100, y_position - 20, f"Tipo: {product.pbano_tipo}")
        c.drawString(100, y_position - 40, f"Marca: {product.pbano_marca}")
        c.drawString(100, y_position - 60, f"Precio: ${product.pbano_precio}")
        c.drawString(100, y_position - 80, f"Cantidad: {product.pbano_cantidad}")
        c.drawString(100, y_position - 100, f"Proveedor: {product.pbano_proveedor}")
        c.drawString(100, y_position - 120, f"Código de Barra: {product.pbano_codigo_barra}")
        c.drawString(100, y_position - 140, f"Material: {product.pbano_material}")
        c.drawString(100, y_position - 160, f"Color: {product.pbano_color}")
        c.drawString(100, y_position - 180, f"Peso: {product.pbano_peso} kg")
        c.drawString(100, y_position - 200, f"Dimensiones: {product.pbano_dimensiones}")
        c.drawString(100, y_position - 220, f"Descripción: {product.pbano_descripcion}")
        c.drawString(100, y_position - 240, f"Uso: {product.pbano_uso}")
        c.drawString(100, y_position - 260, f"Seguridad: {product.pbano_seguridad}")
        c.drawString(100, y_position - 280, f"Stock: {product.pbano_stock}")
        y_position -= 300

    # Finalizar el PDF
    c.save()
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="productos_de_bano.pdf",
        mimetype="application/pdf"
    )