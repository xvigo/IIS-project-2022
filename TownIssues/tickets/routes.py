from email.mime import image
from flask import Blueprint, flash, redirect, url_for, render_template, abort, request
from flask_login import login_required, current_user
from TownIssues.tickets.forms import AddTicketForm, UpdateTicketForm
from TownIssues.models import Ticket
from TownIssues import db
import secrets
import os


tickets = Blueprint('tickets', __name__)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(tickets.root_path, 'static/ticket_pics', picture_fn)
    form_picture.save(picture_path)
    
    return picture_fn


@tickets.route("/tickets/add", methods=['GET', 'POST'])
@login_required
def add_ticket():
    form = AddTicketForm()

    if form.validate_on_submit():
        ticket = Ticket(title=form.title.data, description=form.description.data, street=form.description.data, house_number=form.house_num.data, author=current_user)
        db.session.add(ticket)
        db.session.commit()
        flash('Ticked created succesfully.', 'success')
        return redirect(url_for('main.home'))

    return render_template('update_ticket.html', title='Account', form=form, legend='Create New Ticket')

@tickets.route("/tickets/<int:ticket_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('tickets.ticket_detail', ticket_id=ticket.id))

    return render_template('update_ticket.html', title='Account', form=form, legend='Update Ticket')

@tickets.route("/tickets/<int:ticket_id>")
@login_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    return render_template('ticket_detail.html', title='Account', ticket=ticket, legend='Ticket Details')

@tickets.route("/tickets/<int:ticket_id>/delete", methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.author != current_user:
        abort(403)

    db.session.delete(ticket)
    db.session.commit()
    return redirect(url_for('main.home'))