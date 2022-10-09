from flask import Flask, render_template, flash, redirect, url_for
from TownIssues import auth
from TownIssues.forms import RegistrationForm


import os


posts = [
    {
        'author': 'Autor1',
        'title': 'Issue 1',
        'content': 'Content 1'
    },
    {
        'author': 'Autor2',
        'title': 'Issue 2',
        'content': 'Content 2'
    },
    {
        'author': 'Autor3',
        'title': 'Issue 3',
        'content': 'Content 3'
    }
]
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='b76d4859dd2d340dfe47dbf8993f0386',
        SQLALCHEMY_DATABASE_URI = "postgresql://zrrprrwknjjdep:d143387eaa7912d36c839ea21ca1a22725c86a68c87ecd05ec5f0c54fad453cd@ec2-34-247-72-29.eu-west-1.compute.amazonaws.com:5432/d4fts6bs7pgc1d")

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    global db
    db = SQLAlchemy(app)

    @app.route("/")
    @app.route("/home")
    def home():
        return render_template('home.html', posts=posts)



    @app.route("/register", methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            user = Users(u_name=form.name.data, u_surname=form.surname.data, u_email=form.email.data, u_password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('home'))
        
        return render_template('register.html', title='Register', form=form)

    @app.route("/about")
    def about():
        return render_template('about.html', title='About')

    app.register_blueprint(auth.bp)

    return app


# Create A Model For Table
class Users(db.Model):
    __tablename__ = 'u_user'
    id_user = db.Column(db.Integer, primary_key=True)
    u_name = db.Column(db.String(50))
    u_surname = db.Column(db.String(50))
    u_email = db.Column(db.String(50))
    u_password = db.Column(db.String(50))