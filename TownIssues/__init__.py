from flask import Flask, render_template
from TownIssues import auth

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

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='b76d4859dd2d340dfe47dbf8993f0386',
        #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

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


    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


    @app.route("/")
    @app.route("/home")
    def home():
        return render_template('home.html', posts=posts)


    @app.route("/about")
    def about():
        return render_template('about.html', title='About')

    app.register_blueprint(auth.bp)

    return app
