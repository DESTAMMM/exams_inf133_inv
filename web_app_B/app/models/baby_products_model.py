from database import db

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    proveedor = db.Column(db.String(50), nullable=False)
    codigo_barra = db.Column(db.String(50), nullable=False)

    def __init__(self, nombre, tipo, marca, precio, cantidad, proveedor, codigo_barra):
        self.nombre = nombre
        self.tipo = tipo
        self.marca = marca
        self.precio = precio
        self.cantidad = cantidad
        self.proveedor = proveedor
        self.codigo_barra = codigo_barra

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Product.query.all()

    @staticmethod
    def get_by_id(id):
        return Product.query.get(id)

    def update(self, nombre=None, tipo=None, marca=None, precio=None, cantidad=None, proveedor=None, codigo_barra=None):
        if nombre is not None:
            self.nombre = nombre
        if tipo is not None:
            self.tipo = tipo
        if marca is not None:
            self.marca = marca
        if precio is not None:
            self.precio = precio
        if cantidad is not None:
            self.cantidad = cantidad
        if proveedor is not None:
            self.proveedor = proveedor
        if codigo_barra is not None:
            self.codigo_barra = codigo_barra
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()