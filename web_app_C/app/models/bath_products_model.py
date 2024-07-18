from database import db

class ProductosDeBano(db.Model):
    __tablename__ = "productos_de_bano"
    id = db.Column(db.Integer, primary_key=True)
    pbano_nombre = db.Column(db.String(50), nullable=False)
    pbano_tipo = db.Column(db.String(50), nullable=False)
    pbano_marca = db.Column(db.String(50), nullable=False)
    pbano_precio = db.Column(db.Numeric(10, 2), nullable=False)
    pbano_cantidad = db.Column(db.Integer, nullable=False)
    pbano_proveedor = db.Column(db.String(50), nullable=False)
    pbano_codigo_barra = db.Column(db.String(50), nullable=False)
    pbano_material = db.Column(db.String(50), nullable=False)
    pbano_color = db.Column(db.String(50), nullable=False)
    pbano_peso = db.Column(db.Numeric(10, 2), nullable=False)
    pbano_dimensiones = db.Column(db.String(50), nullable=False)
    pbano_descripcion = db.Column(db.Text, nullable=False)
    pbano_uso = db.Column(db.String(50), nullable=False)
    pbano_seguridad = db.Column(db.String(50), nullable=False)
    pbano_stock = db.Column(db.Integer, nullable=False)

    def __init__(self, nombre, tipo, marca, precio, cantidad, proveedor, codigo_barra,
                 material, color, peso, dimensiones, descripcion,
                 uso, seguridad, stock):
        self.pbano_nombre = nombre
        self.pbano_tipo = tipo
        self.pbano_marca = marca
        self.pbano_precio = precio
        self.pbano_cantidad = cantidad
        self.pbano_proveedor = proveedor
        self.pbano_codigo_barra = codigo_barra
        self.pbano_material = material
        self.pbano_color = color
        self.pbano_peso = peso
        self.pbano_dimensiones = dimensiones
        self.pbano_descripcion = descripcion
        self.pbano_uso = uso
        self.pbano_seguridad = seguridad
        self.pbano_stock = stock

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return ProductosDeBano.query.all()

    @staticmethod
    def get_by_id(id):
        return ProductosDeBano.query.get(id)

    def update(self, nombre=None, tipo=None, marca=None, precio=None, cantidad=None, proveedor=None,
               codigo_barra=None, material=None, color=None, peso=None, dimensiones=None,
               descripcion=None, uso=None, seguridad=None, stock=None):
        if nombre is not None:
            self.pbano_nombre = nombre
        if tipo is not None:
            self.pbano_tipo = tipo
        if marca is not None:
            self.pbano_marca = marca
        if precio is not None:
            self.pbano_precio = precio
        if cantidad is not None:
            self.pbano_cantidad = cantidad
        if proveedor is not None:
            self.pbano_proveedor = proveedor
        if codigo_barra is not None:
            self.pbano_codigo_barra = codigo_barra
        if material is not None:
            self.pbano_material = material
        if color is not None:
            self.pbano_color = color
        if peso is not None:
            self.pbano_peso = peso
        if dimensiones is not None:
            self.pbano_dimensiones = dimensiones
        if descripcion is not None:
            self.pbano_descripcion = descripcion
        if uso is not None:
            self.pbano_uso = uso
        if seguridad is not None:
            self.pbano_seguridad = seguridad
        if stock is not None:
            self.pbano_stock = stock
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()