from flask import Blueprint, abort, redirect, render_template, url_for, flash, request
from TownIssues import db, bcrypt
from flask_login import current_user, login_user, logout_user, login_required
from TownIssues.users.forms import AddUserForm, RegistrationForm, LoginForm, ChangePasswordForm, AccountDetailsForm, UserDetailForm
from TownIssues.models import User, Resident
from TownIssues.users.utils import check_permissions
import os

users = Blueprint('users', __name__)

# Register
@users.route("/register", methods=['GET', 'POST'])
def register():
    # user allready logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Add new resident to db
        new_user = User()
        form.populate_resident_user(new_user)
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', title='Register', form=form)

# Login
@users.route("/login", methods=['GET', 'POST'])
def login():
    # User already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Data submitted in form is valid
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

# Update own account
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account_details():
    profile_form = AccountDetailsForm()
    password_form = ChangePasswordForm()
    if request.method == 'GET':
        profile_form.prefill(current_user)

    elif profile_form.validate_on_submit():
        profile_form.populate_user(current_user)
        db.session.commit()
        flash('Profile info updated succesfully.', 'success')
        return redirect(url_for('users.account_details'))

    elif password_form.validate_on_submit():
        password_correct = bcrypt.check_password_hash(current_user.password, password_form.current_password.data)
        if password_correct:
            hashed_new_password = bcrypt.generate_password_hash(password_form.new_password.data).decode('utf-8')
            current_user.password = hashed_new_password
            db.session.commit()
            flash('Password changed succesfully.', 'success')
            return redirect(url_for('users.account_details'))

        else:
            flash("Couldn't change password, current password is incorrect.", 'danger')

    return render_template('account_details.html', title='Account Details', password_form=password_form, profile_form=profile_form)

# Delete own account
@users.route("/account/delete", methods=['POST'])
@login_required
def delete_account():
    if current_user.role == 'resident':
        for ticket in current_user.resident.tickets:
            for image in ticket.images:
                path = 'TownIssues' + image.url
                if os.path.exists(path):
                    os.remove(path) 

    db.session.delete(current_user)
    db.session.commit()
    return redirect(url_for('users.login'))




# Admin all users lisr
@users.route("/admin/users")
@login_required
def users_list():
    check_permissions(allowed_roles=['admin'])

    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id.desc()).paginate(page=page, per_page=50)
    return render_template('users_list.html', users=users)

@users.route("/admin/users/<int:user_id>", methods=['GET', 'POST'])
@login_required
def user_detail(user_id):
    check_permissions(allowed_roles=['admin'])

    user = User.query.get_or_404(user_id)
    profile_form = UserDetailForm()
    password_form = ChangePasswordForm()
    if request.method == 'GET':
        profile_form.prefill(user)

    elif profile_form.validate_on_submit():
        user_identical_email = User.query.filter_by(email=profile_form.email.data).first()
        profile_form.populate_user(user)

        if user_identical_email is  None or user_identical_email.id == user.id:
            db.session.commit()
            flash('Profile info updated succesfully.', 'success')
        else:
            flash('User with this email address already exists. Please use a different one.', 'danger')

        return redirect(url_for('users.user_detail', user_id=user_id))

    elif password_form.validate_on_submit():
        password_correct = bcrypt.check_password_hash(user.password, password_form.current_password.data)
        if password_correct:
            hashed_new_password = bcrypt.generate_password_hash(password_form.new_password.data).decode('utf-8')
            user.password = hashed_new_password
            db.session.commit()
            flash('Password changed succesfully.', 'success')
            return redirect(url_for('users.user_detail', user_id=user_id))

        else:
            flash("Couldn't change password, current password is incorrect.", 'danger')

    return render_template('user_detail.html', title='User Details', password_form=password_form, profile_form=profile_form, user=user)

@users.route("/admin/users/<int:user_id>/delete", methods=['POST'])
@login_required
def delete_user(user_id):
    check_permissions(allowed_roles=['admin'])
    user = User.query.get_or_404(user_id)
    if user.role == 'resident':
        for ticket in user.resident.tickets:
            for image in ticket.images:
                path = 'TownIssues' + image.url
                if os.path.exists(path):
                    os.remove(path) 
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.users_list'))


# Register
@users.route("/admin/users/add", methods=['GET', 'POST'])
@login_required
def add_user():
    check_permissions(allowed_roles=['admin'])

    form = AddUserForm()
    if form.validate_on_submit():
        # Add new resident to db
        new_user = User()
        form.populate_user(new_user)
        db.session.add(new_user)
        db.session.commit()
        flash(f'User {new_user.name} {new_user.surname}  has been created!', 'success')
        return redirect(url_for('users.users_list'))
    
    return render_template('add_user.html', title='Add User', form=form)