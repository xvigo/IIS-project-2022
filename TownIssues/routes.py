from audioop import add
from flask import abort, render_template, flash, redirect, url_for, request
from sqlalchemy import desc
from TownIssues.forms import RegistrationForm, AddTicketForm, LoginForm, ChangePasswordForm, UpdateAccountForm, UpdateTicketForm
from TownIssues.models import User, Ticket    
from TownIssues import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
    
    
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
    
    
    
@app.route("/")
@app.route("/tickets")
def home():
    tickets = Ticket.query.order_by(desc(Ticket.datetime_created)).all()
    return render_template('tickets.html', tickets=tickets)



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Add new user to DB
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, surname=form.surname.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Email or password is incorrect. Please try again.', 'danger')
    return render_template('login.html', title='Log In', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('account'))

    elif password_form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, password_form.current_password.data):
            hashed_pwd = bcrypt.generate_password_hash(password_form.new_password.data).decode('utf-8')
            current_user.password = hashed_pwd
            db.session.commit()
            flash('Password changed succesfully.', 'success')
            return redirect(url_for('account'))

        else:
            flash("Couldn't change password, current password is incorrect.", 'danger')

    return render_template('account.html', title='Account', password_form=password_form, profile_form=profile_form)

@app.route("/tickets/add", methods=['GET', 'POST'])
@login_required
def add_ticket():
    form = AddTicketForm()


    if form.validate_on_submit():
        ticket = Ticket(title=form.title.data, description=form.description.data, street=form.description.data, house_number=form.house_num.data, author=current_user)
        db.session.add(ticket)
        db.session.commit()
        flash('Ticked created succesfully.', 'success')
        return redirect(url_for('home'))

    return render_template('update_ticket.html', title='Account', form=form, legend='Create New Ticket')

@app.route("/tickets/<int:ticket_id>/update", methods=['GET', 'POST'])
@login_required
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.author != current_user:
        abort(403)

    form = UpdateTicketForm()
    if request.method == 'GET':
        form.title.data = ticket.title
        form.description.data = ticket.description
        form.street.data = ticket.street
        form.house_num.data = ticket.house_number

    elif form.validate_on_submit():
        ticket.title = form.title.data
        ticket.description = form.description.data
        ticket.street = form.street.data
        ticket.house_number = form.house_num.data
        db.session.commit()
        flash('Ticket updated succesfully.', 'success')
        return redirect(url_for('home'))

    return render_template('update_ticket.html', title='Account', form=form, legend='Update Ticket')

