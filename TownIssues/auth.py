import functools
from TownIssues.forms import RegistrationForm, LoginForm

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
#from werkzeug.security import check_password_hash, generate_password_hash

#from flaskr.db import get_db

bp = Blueprint('auth', __name__)


@bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.email.data}', 'success')
        return redirect(url_for('home'))
        
    return render_template('register.html', title='Register', form=form)

@bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Log In', form=form)