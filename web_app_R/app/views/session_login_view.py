from flask import render_template
from flask_login import current_user

def usuarios(session_logins):
    return render_template(
        "usuarios.html",
        sessions=session_logins,
        title="Lista de usuarios",
        current_user=current_user,
    )

def registro():
    return render_template(
        "registro.html", title="Registro de usuarios", current_user=current_user
    )

def actualizar(session_login):
    return render_template(
        "actualizar.html",
        title="Actualizar usuario",
        session_login=session_login,
        current_user=current_user,
    )

def login():
    return render_template(
        "login.html", title="Inicio de sesión", current_user=current_user
    )

def perfil(session_login):
    return render_template(
        "profile.html", title="Perfil de usuario", current_user=current_user, session=session_login
    )