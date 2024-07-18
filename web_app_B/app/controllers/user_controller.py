from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from utils.decorators import role_required
from views import user_view
from models.user_model import User

user_bp = Blueprint("user", __name__)

@user_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for(".profiuserle", id=current_user.correo))
    return redirect(url_for("user.login"))

@user_bp.route("/users")
@login_required
def list_users():
    users = User.get_all()
    return user_view.usuarios(users)

@user_bp.route("/users/create", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        correo = request.form["correo"]
        name = request.form["name"]
        password = request.form["password"]
        role = request.form["role"]
        existing_user = User.get_user_by_correo(correo)
        if existing_user:
            flash("El correo ya está en uso", "error")
            return redirect(url_for("user.create_user"))
        user = User(correo=correo, name=name, password=password, role=role)
        user.set_password(password)
        user.save()
        flash("Usuario registrado exitosamente", "success")
        return redirect(url_for("user.list_users"))
    return user_view.registro()

@user_bp.route("/users/<string:correo>/update", methods=["GET", "POST"])
@login_required
@role_required("admin")
def update_user(correo):
    user = User.get_user_by_correo(correo)
    if not user:
        return "Usuario no encontrado", 404
    if request.method == "POST":
        name = request.form["name"]
        role = request.form["role"]
        user.name = name
        user.role = role
        user.update()
        return redirect(url_for("user.list_users"))
    return user_view.actualizar(user)

@user_bp.route("/users/<string:correo>/delete")
@login_required
@role_required("admin")
def delete_user(correo):
    user = User.get_user_by_correo(correo)
    if not user:
        return "Usuario no encontrado", 404
    user.delete()
    return redirect(url_for("user.list_users"))

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]
        user = User.get_user_by_correo(correo)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Inicio de sesión exitoso", "success")
            if user.has_role("admin"):
                return redirect(url_for("user.list_users"))
            else:
                return redirect(url_for("user.profile", correo=user.correo))
        else:
            flash("Correo o contraseña incorrectos", "error")
    return user_view.login()

@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for("user.login"))

@user_bp.route("/profile/<string:correo>")
@login_required
def profile(correo):
    user = User.get_user_by_correo(correo)
    return user_view.perfil(user)