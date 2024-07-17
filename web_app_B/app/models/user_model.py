from datetime import datetime, timezone
from database import db
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    correo = db.Column(db.String(255), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    registration_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    role = db.Column(db.String(50), nullable=False, default="user")

    def __init__(self, correo, name, password, role="user"):
        self.correo = correo
        self.name = name
        self.set_password(password)
        self.registration_date = datetime.now(timezone.utc)
        self.role = role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_user_by_correo(correo):
        return User.query.filter_by(correo=correo).first()

    def has_role(self, role):
        return self.role == role

    def get_id(self):
        return self.correo