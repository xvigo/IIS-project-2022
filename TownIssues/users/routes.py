from flask import Blueprint, redirect, render_template, url_for, flash, request
from TownIssues import bcrypt
from flask_login import current_user, login_user, logout_user, login_required
from TownIssues.users.forms import AddUserForm, RegistrationForm, LoginForm, \
     AddTechnicianForm, ChangePasswordForm, SetPasswordForm, AccountDetailsForm
from TownIssues.users import service
from TownIssues.models import User
from TownIssues.users.utils import check_permissions

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    """Route for registering new residents."""
    # User already logged in -> redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Add new resident to db
        new_user = User()
        form.populate_resident_user(new_user)
        service.add_user(new_user)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    """Route for logging in any user."""
    # User already logged in -> redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = service.get_user(email=form.email.data)

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            # Redirect to page which unauthenticated user originally tried to access 
            next_page = request.args.get('next', url_for('main.home'))
            return redirect(next_page)
        else:
            flash('Email or password is incorrect. Please try again.', 'danger')

    return render_template('login.html', title='Log In', form=form)


@users.route("/logout")
def logout():
    """Route that performs logout and immediately redirects to login page."""
    logout_user()
    return redirect(url_for('users.login'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account_details():
    """Route for viewing and updating users account details."""
    profile_form = AccountDetailsForm()
    password_form = ChangePasswordForm()

    if profile_form.submitted() and profile_form.validate():
        profile_form.populate_user(current_user)
        service.update()
        flash('Profile info updated successfully.', 'success')
        return redirect(url_for('users.account_details'))

    if password_form.submitted() and password_form.validate():
        password_correct = bcrypt.check_password_hash(current_user.password, password_form.current_password.data)
        if password_correct:
            hashed_new_password = bcrypt.generate_password_hash(password_form.new_password.data).decode('utf-8')
            current_user.password = hashed_new_password
            service.update()
            flash('Password changed successfully.', 'success')

        else:
            flash("Submitted current password is incorrect. Try again.", 'danger')
        return redirect(url_for('users.account_details'))


    profile_form.prefill(current_user)
    return render_template('account_details.html', title='Account Details', password_form=password_form, profile_form=profile_form)


@users.route("/account/delete", methods=['POST'])
@login_required
def delete_account():
    """Route for deleting users own account."""
    service.delete_user(current_user)
    return redirect(url_for('users.login'))


#### ADMIN ONLY
@users.route("/admin/users")
@login_required
def users_list():
    """Admin route for viewing all users using pagination."""
    check_permissions(allowed_roles=['admin'])

    page = request.args.get('page', 1, type=int)
    users = service.get_users_list(page)
    return render_template('users_list.html', users=users)


@users.route("/admin/users/<int:user_id>", methods=['GET', 'POST'])
@login_required
def user_detail(user_id):
    """Admin route for viewing details of the selected user."""
    check_permissions(allowed_roles=['admin'])

    user = service.get_user_or_404(user_id=user_id)
    profile_form = AccountDetailsForm()
    password_form = SetPasswordForm()

    if profile_form.submitted() and profile_form.validate():
        user_identical_email = service.get_user(email=profile_form.email.data)
        if user_identical_email is  None or user_identical_email.id == user.id:
            profile_form.populate_user(user)
            service.update()
            flash('Profile info updated successfully.', 'success')
        else:
            flash('User with this email address already exists. Please use a different one.', 'danger')
        return redirect(url_for('users.user_detail', user_id=user_id))

    if password_form.submitted() and password_form.validate():
        hashed_new_password = bcrypt.generate_password_hash(password_form.new_password.data).decode('utf-8')
        user.password = hashed_new_password
        service.update()
        flash('Password changed successfully.', 'success')
        return redirect(url_for('users.user_detail', user_id=user_id))

    profile_form.prefill(user)
    return render_template('user_detail.html', title='User Details', password_form=password_form, profile_form=profile_form, user=user)


@users.route("/admin/users/<int:user_id>/delete", methods=['POST'])
@login_required
def delete_user(user_id):
    """Admin route dor deleting users, immediately redirects to users list."""
    check_permissions(allowed_roles=['admin'])

    user = service.get_user_or_404(user_id=user_id)
    service.delete_user(user)
    return redirect(url_for('users.users_list'))


@users.route("/admin/users/add", methods=['GET', 'POST'])
@login_required
def add_user():
    """Admin route for adding new user."""
    check_permissions(allowed_roles=['admin'])

    form = AddUserForm()
    if form.validate_on_submit():
        # Add new resident to db
        new_user = User()
        form.populate_user(new_user)
        service.add_user(new_user)
        flash(f'User {new_user.name} {new_user.surname}  has been created!', 'success')
        return redirect(url_for('users.users_list'))
    
    return render_template('add_user.html', title='Add User', form=form)


#### MANAGER ONLY
@users.route("/add_technician", methods=['GET', 'POST'])
@login_required
def add_technician():
    """Manager route for adding technicians."""
    check_permissions(allowed_roles=['manager'])

    form = AddTechnicianForm()
    if form.validate_on_submit():
        # Add new resident to db
        new_user = User()
        form.populate_user(new_user)
        service.add_user(new_user)
        flash(f'Technician {new_user.name} {new_user.surname}  has been created!', 'success')
        return redirect(url_for('users.technicians_list'))
    
    return render_template('add_service_technician.html', title='Add Technician', form=form)

@users.route("/technicians")
@login_required
def technicians_list():
    """Manager route for viewing all users using pagination."""
    check_permissions(allowed_roles=['manager'])

    page = request.args.get('page', 1, type=int)
    users = service.get_users_list(page=page, role="technician")
    return render_template('technicians_list.html', users=users)
