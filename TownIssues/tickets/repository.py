from pydoc import doc
from TownIssues import db
from flask_login import  current_user
from TownIssues.models import Ticket
from TownIssues.tickets.forms import AddTicketForm, UpdateTicketForm


def db_add_ticket_from_form(form):
    
    if not isinstance(form, AddTicketForm):
        raise TypeError 

    ticket = Ticket(title=form.title.data, 
                    content=form.content.data, 
                    street=form.street.data, 
                    house_number=form.house_num.data,
                    author=current_user.resident)

    db.session.add(ticket)
    db.session.commit()

def db_update_ticket_from_form(ticket, form):
    if not isinstance(form, AddTicketForm):
        raise TypeError 

    ticket.title = form.title.data
    ticket.content = form.content.data
    ticket.street = form.street.data
    ticket.house_number = form.house_num.data
    db.session.commit()

def db_delete_ticket(ticket):
    db.session.delete(ticket)
    db.session.commit()

def db_get_ticket_or_404(ticket_id):
    return Ticket.query.get_or_404(ticket_id)