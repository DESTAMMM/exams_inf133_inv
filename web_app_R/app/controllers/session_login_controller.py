from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from models.session_login_model import SessionLogin
from views import session_login_view
from utils.decorators import role_required

session_bp = Blueprint("session", __name__)

@session_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("session.profile", correo=current_user.correo_principal))
    return redirect(url_for("session.login"))

@session_bp.route("/sessions")
@login_required
def list_sessions():
    sessions = SessionLogin.get_all()
    return session_login_view.usuarios(sessions)

@session_bp.route("/sessions/create", methods=["GET", "POST"])
def create_session():
    if request.method == "POST":
        correo = request.form["correo"]
        name = request.form["name"]
        password = request.form["password"]
        rol = request.form["role"]
        #comprobando si ya hay un usuario creado con el mismo correo
        existing_user = SessionLogin.get_session_by_correo(correo)
        #si ya hay uno entonces redirige de nuevo para crear un nuevo usuario
        if existing_user:
            flash("El correo ya está en uso", "error")
            return redirect(url_for("session.create_session"))
        #almacenando los datos del usuario
        session = SessionLogin(correo_principal=correo, nombre_usuario=name, password=password, rol=rol)
        #generando un hash seguro para la contrasena
        session.set_password(password)
        #almacenando el usuario en la base de datos
        session.save()
        flash("Usuario registrado exitosamente", "success")
        return redirect(url_for("session.list_sessions"))
    return session_login_view.registro()

@session_bp.route("/sessions/<string:correo>/update", methods=["GET", "POST"])
@login_required
@role_required("admin")
def update_session(correo):
    session = SessionLogin.get_session_by_correo(correo)
    if not session:
        return "Usuario no encontrado", 404
    if request.method == "POST":
        name = request.form["name"]
        rol = request.form["role"]  # Agregar captura del rol desde el formulario
        session.nombre_usuario = name
        session.rol = rol
        session.update()
        return redirect(url_for("session.list_sessions"))
    return session_login_view.actualizar(session)

@session_bp.route("/sessions/<string:correo>/delete", methods=["GET", "POST"])
@login_required
@role_required("admin")
def delete_session(correo):
    session = SessionLogin.get_session_by_correo(correo)
    if not session:
        return "Usuario no encontrado", 404
    session.delete()
    return redirect(url_for("session.list_sessions"))

@session_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]
         # Busca la sesión de usuario en la base de datos usando el correo proporcionado
        session = SessionLogin.get_session_by_correo(correo)
         # Verifica si la sesión existe y si la contraseña proporcionada es correcta
        if session and check_password_hash(session.password_hash, password):
            login_user(session)
            flash("Inicio de sesión exitoso", "success")
            #verificacion de roles 
            if session.has_role("admin"):
                return redirect(url_for("session.list_sessions"))
            else:
                return redirect(url_for("session.profile", correo=session.correo_principal))
        else:
            flash("Correo o contraseña incorrectos", "error")
    return session_login_view.login()

@session_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for("session.login"))

@session_bp.route("/profile/<string:correo>")
@login_required
def profile(correo):
    session = SessionLogin.get_session_by_correo(correo)
    if not session:
        return "Usuario no encontrado", 404
    return session_login_view.perfil(session)