from flask import Flask
from flask_login import LoginManager

from controllers import session_login_controller
from controllers import bath_products_controller
from database import db
from models.session_login_model import SessionLogin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "clave-secreta-we"

login_manager = LoginManager()
login_manager.login_view = "SessionLogin.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(correo):
    return SessionLogin.get_user_by_correo(correo)

db.init_app(app)

app.register_blueprint(session_login_controller.session_login_bp)
app.register_blueprint(bath_products_controller.bath_product_bp )

if __name__ == "__main__":

    with app.app_context():
        db.create_all()
    app.run(debug=True)