from flask import Blueprint, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from models.children_books_model import LibrosInfantiles
from views import children_books_view
from utils.decorators import role_required

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

from flask import Blueprint

children_books_bp = Blueprint("children_books", __name__)

@children_books_bp.route("/children_books")
@login_required
def list_books():
    books = LibrosInfantiles.get_all()
    return children_books_view.list_books(books)

@children_books_bp.route("/children_books/create", methods=["GET", "POST"])
@login_required
@role_required("admin")
def create_book():
    if request.method == "POST":
        if current_user.has_role("admin"):
            titulo = request.form["titulo"]
            autor = request.form["autor"]
            genero = request.form["genero"]
            precio = float(request.form["precio"])
            cantidad = int(request.form["cantidad"])
            editorial = request.form["editorial"]
            codigo_barra = request.form["codigo_barra"]
            idioma = request.form["idioma"]
            paginas = int(request.form["paginas"])
            formato = request.form["formato"]
            isbn = request.form["isbn"]
            descripcion = request.form["descripcion"]
            proveedor = request.form["proveedor"]
            stock = int(request.form["stock"])
            edad_recomendada = request.form["edad_recomendada"]
            
            book = LibrosInfantiles(
                titulo=titulo,
                autor=autor,
                genero=genero,
                precio=precio,
                cantidad=cantidad,
                editorial=editorial,
                codigo_barra=codigo_barra,
                idioma=idioma,
                paginas=paginas,
                formato=formato,
                isbn=isbn,
                descripcion=descripcion,
                proveedor=proveedor,
                stock=stock,
                edad_recomendada=edad_recomendada
            )
            book.save()
            flash("Libro creado exitosamente", "success")
            return redirect(url_for("children_books.list_books"))
        else:
            return jsonify({"message": "Unauthorized"}), 403
    return children_books_view.create_book()

@children_books_bp.route("/children_books/<int:id>/update", methods=["GET", "POST"])
@login_required
@role_required("admin")
def update_book(id):
    book = LibrosInfantiles.get_by_id(id)
    if not book:
        return "Libro no encontrado", 404
    if request.method == "POST":
        if current_user.has_role("admin"):
            book.lin_titulo = request.form["titulo"]
            book.lin_autor = request.form["autor"]
            book.lin_genero = request.form["genero"]
            book.lin_precio = float(request.form["precio"])
            book.lin_cantidad = int(request.form["cantidad"])
            book.lin_editorial = request.form["editorial"]
            book.lin_codigo_barra = request.form["codigo_barra"]
            book.lin_idioma = request.form["idioma"]
            book.lin_paginas = int(request.form["paginas"])
            book.lin_formato = request.form["formato"]
            book.lin_isbn = request.form["isbn"]
            book.lin_descripcion = request.form["descripcion"]
            book.lin_proveedor = request.form["proveedor"]
            book.lin_stock = int(request.form["stock"])
            book.lin_edad_recomendada = request.form["edad_recomendada"]
            
            book.update()
            flash("Libro actualizado exitosamente", "success")
            return redirect(url_for("children_books.list_books"))
        else:
            return jsonify({"message": "Unauthorized"}), 403
    return children_books_view.update_book(book)

@children_books_bp.route("/children_books/<int:id>/delete")
@login_required
@role_required("admin")
def delete_book(id):
    book = LibrosInfantiles.get_by_id(id)
    if not book:
        return "Libro no encontrado", 404
    if current_user.has_role("admin"):
        book.delete()
        flash("Libro eliminado exitosamente", "success")
        return redirect(url_for("children_books.list_books"))
    else:
        return jsonify({"message": "Unauthorized"}), 403
    
@children_books_bp.route("/children_books/download_pdf")
@login_required
@role_required("admin")
def download_pdf():
    buffer = BytesIO()
    # Cambiar el tamaño de la página a horizontal (landscape)
    doc = SimpleDocTemplate(buffer, pagesize=(14*inch, 11*inch))  # Tamaño personalizado en pulgadas
    data = []
    headers = ["ID", "Título", "Autor", "Género", "Precio", "Cantidad", "Editorial", "Código de Barra", "Idioma", "Páginas", "Formato", "ISBN", "Descripción", "Proveedor", "Stock", "Edad Recomendada"]
    data.append(headers)

    # Obtener todos los libros
    books = LibrosInfantiles.get_all()

    # Añadir libros a la tabla
    for book in books:
        row = [
            book.id, 
            book.lin_titulo,
            book.lin_autor,
            book.lin_genero,
            f"${book.lin_precio}",
            book.lin_cantidad,
            book.lin_editorial,
            book.lin_codigo_barra,
            book.lin_idioma,
            book.lin_paginas,
            book.lin_formato,
            book.lin_isbn,
            book.lin_descripcion,
            book.lin_proveedor,
            book.lin_stock,
            book.lin_edad_recomendada
        ]
        data.append(row)

    # Crear la tabla
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Crear el documento PDF
    elements = [table]
    doc.build(elements)

    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="libros_infantiles.pdf",
        mimetype="application/pdf"
    )