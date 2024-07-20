from database import db

class LibrosInfantiles(db.Model):
    __tablename__ = "libros_infantiles"
    id = db.Column(db.Integer, primary_key=True)
    lin_titulo = db.Column(db.String(50), nullable=False)
    lin_autor = db.Column(db.String(50), nullable=False)
    lin_genero = db.Column(db.String(50), nullable=False)
    lin_precio = db.Column(db.Numeric(10, 2), nullable=False)
    lin_cantidad = db.Column(db.Integer, nullable=False)
    lin_editorial = db.Column(db.String(50), nullable=False)
    lin_codigo_barra = db.Column(db.String(50), nullable=False)
    lin_idioma = db.Column(db.String(50), nullable=False)
    lin_paginas = db.Column(db.Integer, nullable=False)
    lin_formato = db.Column(db.String(50), nullable=False)
    lin_isbn = db.Column(db.String(50), nullable=False)
    lin_descripcion = db.Column(db.Text, nullable=False)
    lin_proveedor = db.Column(db.String(50), nullable=False)
    lin_stock = db.Column(db.Integer, nullable=False)
    lin_edad_recomendada = db.Column(db.String(50), nullable=False)

    def __init__(self, titulo, autor, genero, precio, cantidad, editorial, 
                 codigo_barra, idioma, paginas, formato, isbn, 
                 descripcion, proveedor, stock, edad_recomendada):
        self.lin_titulo = titulo
        self.lin_autor = autor
        self.lin_genero = genero
        self.lin_precio = precio
        self.lin_cantidad = cantidad
        self.lin_editorial = editorial
        self.lin_codigo_barra = codigo_barra
        self.lin_idioma = idioma
        self.lin_paginas = paginas
        self.lin_formato = formato
        self.lin_isbn = isbn
        self.lin_descripcion = descripcion
        self.lin_proveedor = proveedor
        self.lin_stock = stock
        self.lin_edad_recomendada = edad_recomendada

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return LibrosInfantiles.query.all()

    @staticmethod
    def get_by_id(id):
        return LibrosInfantiles.query.get(id)

    def update(self, titulo=None, autor=None, genero=None, precio=None, cantidad=None, editorial=None, 
               codigo_barra=None, idioma=None, paginas=None, formato=None, isbn=None, 
               descripcion=None, proveedor=None, stock=None, edad_recomendada=None):
        if titulo is not None:
            self.lin_titulo = titulo
        if autor is not None:
            self.lin_autor = autor
        if genero is not None:
            self.lin_genero = genero
        if precio is not None:
            self.lin_precio = precio
        if cantidad is not None:
            self.lin_cantidad = cantidad
        if editorial is not None:
            self.lin_editorial = editorial
        if codigo_barra is not None:
            self.lin_codigo_barra = codigo_barra
        if idioma is not None:
            self.lin_idioma = idioma
        if paginas is not None:
            self.lin_paginas = paginas
        if formato is not None:
            self.lin_formato = formato
        if isbn is not None:
            self.lin_isbn = isbn
        if descripcion is not None:
            self.lin_descripcion = descripcion
        if proveedor is not None:
            self.lin_proveedor = proveedor
        if stock is not None:
            self.lin_stock = stock
        if edad_recomendada is not None:
            self.lin_edad_recomendada = edad_recomendada
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()