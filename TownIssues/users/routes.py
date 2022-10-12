from flask import Blueprint, redirect, render_template, url_for, flash, request
from TownIssues import db, bcrypt
from flask_login import current_user, login_user, logout_user, login_required
from TownIssues.users.forms import RegistrationForm, LoginForm, ChangePasswordForm, UpdateAccountForm
from TownIssues.models import User, Resident

users = Blueprint('users', __name__)

# Register
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Add new user to DB
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, surname=form.surname.data, email=form.email.data, password=hashed_pwd, role='resident', resident=Resident())
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', title='Register', form=form)


# Login
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next', url_for('main.home'))
            return redirect(next_page)
        else:
            flash('Email or password is incorrect. Please try again.', 'danger')
    return render_template('login.html', title='Log In', form=form)

# Logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))

# Update account
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    password_form = ChangePasswordForm()
    profile_form = UpdateAccountForm()
    if request.method == 'GET':
        profile_form.name.data = current_user.name
        profile_form.surname.data = current_user.surname
        profile_form.email.data = current_user.email

    elif profile_form.validate_on_submit():
        current_user.name = profile_form.name.data
        current_user.surname = profile_form.surname.data
        current_user.email = profile_form.email.data
        db.session.commit()
        flash('Profile info updated succesfully.', 'success')
        return redirect(url_for('users.account'))

    elif password_form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, password_form.current_password.data):
            hashed_pwd = bcrypt.generate_password_hash(password_form.new_password.data).decode('utf-8')
            current_user.password = hashed_pwd
            db.session.commit()
            flash('Password changed succesfully.', 'success')
            return redirect(url_for('users.account'))

        else:
            flash("Couldn't change password, current password is incorrect.", 'danger')

    return render_template('account.html', title='Account', password_form=password_form, profile_form=profile_form)

@users.route("/account/delete", methods=['POST'])
@login_required
def delete_account():
    db.session.delete(current_user)
    db.session.commit()
    return redirect(url_for('users.login'))


# Detail of ticket
@users.route("/admin/user/<int:user_id>",  methods=['GET', 'POST'])
@login_required
def user_detail(user_id):
    user =  User.query.get_or_404(user_id)
    password_form = ChangePasswordForm()
    profile_form = UpdateAccountForm()
    
    if request.method == 'GET':
        profile_form.name.data = user.name
        profile_form.surname.data = user.surname
        profile_form.email.data = user.email

    elif profile_form.validate_on_submit():
        user.name = profile_form.name.data
        user.surname = profile_form.surname.data
        user.email = profile_form.email.data
        db.session.commit()
        flash('Profile info updated succesfully.', 'success')
        return redirect(url_for('users.account'))

    elif password_form.validate_on_submit():
        if bcrypt.check_password_hash(user.password, password_form.current_password.data):
            hashed_pwd = bcrypt.generate_password_hash(password_form.new_password.data).decode('utf-8')
            user.password = hashed_pwd
            db.session.commit()
            flash('Password changed succesfully.', 'success')
            return redirect(url_for('users.account'))

        else:
            flash("Couldn't change password, current password is incorrect.", 'danger')

    return render_template('account.html', title='Account', password_form=password_form, profile_form=profile_form)


# Detail of ticket
@users.route("/admin/users")
@login_required
def users_list():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id.desc()).paginate(page=page, per_page=10)
    return render_template('users_list.html', users=users)

# Register
@users.route("/admin/users/add", methods=['GET', 'POST'])
def add_user():

    form = RegistrationForm()
    if form.validate_on_submit():
        # Add new user to DB
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, surname=form.surname.data, email=form.email.data, password=hashed_pwd, role='resident', resident=Resident())
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', title='Add new user', form=form)
