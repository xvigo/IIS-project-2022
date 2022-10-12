from flask import Blueprint, flash, redirect, url_for, render_template, abort, request
from flask_login import login_required, current_user
from TownIssues.tickets.forms import AddTicketForm, UpdateTicketForm
from TownIssues.models import Ticket
from TownIssues import db
from TownIssues.tickets.repository import db_add_ticket_from_form, db_delete_ticket, db_update_ticket_from_form, db_get_ticket_or_404

tickets = Blueprint('tickets', __name__)

# Add ticket
@tickets.route("/tickets/add", methods=['GET', 'POST'])
@login_required
def add_ticket():
    form = AddTicketForm()

    if form.validate_on_submit():
        db_add_ticket_from_form(form)
        flash('Ticked created succesfully.', 'success')
        return redirect(url_for('tickets.tickets_list'))

    return render_template('update_ticket.html', title='Account', form=form, legend='Create New Ticket')

# Update ticket
@tickets.route("/tickets/<int:ticket_id>/update", methods=['GET', 'POST'])
@login_required
def update_ticket(ticket_id):
    ticket = db_get_ticket_or_404(ticket_id)
    if ticket.author != current_user.resident:
        abort(403)

    form = UpdateTicketForm()
    if request.method == 'GET':
        form.prefill(ticket)

    elif form.validate_on_submit():
        db_update_ticket_from_form(ticket, form)
        flash('Ticket updated succesfully.', 'success')
        return redirect(url_for('tickets.ticket_detail', ticket_id=ticket.id))

    return render_template('update_ticket.html', title='Account', form=form, legend='Update Ticket')

# Delete ticket
@tickets.route("/tickets/<int:ticket_id>/delete", methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = db_get_ticket_or_404(ticket_id)
    if ticket.author != current_user.resident:
        abort(403)

    db_delete_ticket(ticket)
    return redirect(url_for('main.home'))

# Detail of ticket
@tickets.route("/tickets/<int:ticket_id>")
@login_required
def ticket_detail(ticket_id):
    ticket = db_get_ticket_or_404(ticket_id)
    return render_template('ticket_detail.html', title='Account', ticket=ticket, legend='Ticket Details')


@tickets.route("/tickets")
@login_required
def tickets_list():
    page = request.args.get('page', 1, type=int)
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).paginate(page=page, per_page=5)
    return render_template('tickets_list.html', tickets=tickets)