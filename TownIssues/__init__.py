from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_class=None):
    app = Flask(__name__)

    if config_class is None:
        from TownIssues.config import Config
        config_class = Config

    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = "warning"

    from TownIssues.main.routes import main
    from TownIssues.users.routes import users
    from TownIssues.tickets.routes import tickets
    from TownIssues.errors.handlers import errors
    from TownIssues.service_requests.routes import service_requests

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(tickets)
    app.register_blueprint(errors)
    app.register_blueprint(service_requests)

    return app