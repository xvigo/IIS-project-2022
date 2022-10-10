import bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# from os import makedirs

# def create_app(test_config=None):
#     #create and configure the app
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         SECRET_KEY='b76d4859dd2d340dfe47dbf8993f0386',
#         SQLALCHEMY_DATABASE_URI = "postgresql://zrrprrwknjjdep:d143387eaa7912d36c839ea21ca1a22725c86a68c87ecd05ec5f0c54fad453cd@ec2-34-247-72-29.eu-west-1.compute.amazonaws.com:5432/d4fts6bs7pgc1d")

#     if test_config is None:
#         # load the instance config, if it exists, when not testing
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         # load the test config if passed in
#         app.config.from_mapping(test_config)

#     # ensure the instance folder exists
#     try:
#         makedirs(app.instance_path)
#     except OSError:
#         pass

#     global db
#     db = SQLAlchemy(app)

#     return app

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='b76d4859dd2d340dfe47dbf8993f0386',
    SQLALCHEMY_DATABASE_URI = "postgresql://xrazzggtkegawp:38c7259d2fb0f773960265fa484c1725954e22d58496cc988aa6697a8c4f6b6a@ec2-54-194-180-51.eu-west-1.compute.amazonaws.com:5432/dfur7dcgfmutjb")
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "warning"


from TownIssues import routes