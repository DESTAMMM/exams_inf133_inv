from datetime import datetime, timezone
from database import db
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

class SessionLogin(UserMixin,db.Model):
    __tablename__ = "login_recuperatorio"
    correo_principal = db.Column(db.String(255), unique=True, primary_key=True)
    nombre_usuario = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, correo_principal, nombre_usuario, password, rol):
        self.correo_principal = correo_principal
        self.nombre_usuario = nombre_usuario
        self.rol = rol
        self.set_password(password)
        self.registration_date = datetime.now(timezone.utc)

    def set_password(self, password):
        # generando un hash seguro y almacenable
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
        return self.rol == role
    
    @staticmethod
    def get_session_by_correo(correo_principal):
        return SessionLogin.query.filter_by(correo_principal=correo_principal).first()
    
    def get_id(self):
        return self.correo_principal