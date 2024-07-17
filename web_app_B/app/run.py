from flask import Flask
from flask_login import LoginManager

from controllers import user_controller
from controllers import baby_products_controller
from database import db
from models.user_model import User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "clave-secreta-we"

login_manager = LoginManager()
login_manager.login_view = "user.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(correo):
    return User.get_user_by_correo(correo)

db.init_app(app)

app.register_blueprint(user_controller.user_bp)
app.register_blueprint(baby_products_controller.product_bp)

if __name__ == "__main__":

    with app.app_context():
        db.create_all()
    app.run(debug=True)