from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models.session_login_model import SessionLogin
from views import session_login_view
from utils.decorators import role_required

session_login_bp = Blueprint("session_login", __name__)

@session_login_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("session_login.profile", correo=current_user.cuenta_correo))
    return redirect(url_for("session_login.login"))

@session_login_bp.route("/session_logins")
@login_required
def list_session_logins():
    session_logins = SessionLogin.get_all()
    return session_login_view.usuarios(session_logins)

@session_login_bp.route("/session_logins/create", methods=["GET", "POST"])
@login_required
def create_session_login():
    if request.method == "POST":
        correo = request.form["correo"]
        name = request.form["name"]
        password = request.form["password"]
        rol = request.form["rol"]
        existing_user = SessionLogin.get_session_by_correo(correo)
        if existing_user:
            flash("El correo ya está en uso", "error")
            return redirect(url_for("session_login.create_session_login"))
        session_login = SessionLogin(cuenta_correo=correo, nombre_usuario=name, password=password, rol=rol)
        session_login.set_password(password)
        session_login.save()
        flash("Usuario registrado exitosamente", "success")
        return redirect(url_for("session_login.list_session_logins"))
    return session_login_view.registro()

@session_login_bp.route("/session_logins/<string:correo>/update", methods=["GET", "POST"])
@login_required
@role_required("admin")
def update_session_login(correo):
    session_login = SessionLogin.get_session_by_correo(correo)
    if not session_login:
        return "Usuario no encontrado", 404
    if request.method == "POST":
        name = request.form["name"]
        rol = request.form["role"]  # Agregar captura del rol desde el formulario
        session_login.nombre_usuario = name
        session_login.rol = rol
        session_login.update()
        return redirect(url_for("session_login.list_session_logins"))
    return session_login_view.actualizar(session_login)

@session_login_bp.route("/session_logins/<string:correo>/delete", methods=["GET", "POST"])
@login_required
@role_required("admin")
def delete_session_login(correo):
    session_login = SessionLogin.get_session_by_correo(correo)
    if not session_login:
        return "Usuario no encontrado", 404
    session_login.delete()
    return redirect(url_for("session_login.list_session_logins"))

@session_login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]
        session_login = SessionLogin.get_session_by_correo(correo)
        if session_login and check_password_hash(session_login.password_hash, password):
            login_user(session_login)
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("session_login.profile", correo=session_login.cuenta_correo))
        else:
            flash("Correo o contraseña incorrectos", "error")
    return session_login_view.login()

@session_login_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for("session_login.login"))

@session_login_bp.route("/profile/<string:correo>")
@login_required
def profile(correo):
    session_login = SessionLogin.get_session_by_correo(correo)
    if not session_login:
        return "Usuario no encontrado", 404
    return session_login_view.perfil(session_login)