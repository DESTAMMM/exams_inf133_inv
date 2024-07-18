from datetime import datetime, timezone
from database import db
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

class SessionLogin(UserMixin,db.Model):
    __tablename__ = "sessiones_login"
    cuenta_correo = db.Column(db.String(255), unique=True, primary_key=True)
    nombre_usuario = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False, default="user")
    registration_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, cuenta_correo, nombre_usuario, password, rol):
        self.cuenta_correo = cuenta_correo
        self.nombre_usuario = nombre_usuario
        self.rol = rol
        self.set_password(password)
        self.registration_date = datetime.now(timezone.utc)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return SessionLogin.query.all()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def has_role(self, role):
        return self.role == role
    
    @staticmethod
    def get_session_by_correo(cuenta_correo):
        return SessionLogin.query.filter_by(cuenta_correo=cuenta_correo).first()