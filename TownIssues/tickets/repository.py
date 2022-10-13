from pydoc import doc

from flask import current_app
from TownIssues import db
from flask_login import  current_user
from TownIssues.models import Image, Ticket
from TownIssues.tickets.forms import AddTicketForm, UpdateTicketForm
import os
import secrets

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/ticket_pics/' + picture_fn)
    form_picture.save(picture_path)
    
    return picture_fn


def db_add_ticket_from_form(form):
    
    if not isinstance(form, AddTicketForm):
        raise TypeError 
    
    
    ticket = Ticket(title=form.title.data,
                    content=form.content.data,
                    street=form.street.data, 
                    house_number=form.house_num.data,
                    author=current_user.resident)

    for form_image in form.picture.data:
        picture = save_picture(form_image)
        image = Image(url='/static/ticket_pics/' + picture)
        ticket.images.append(image)

    db.session.add(ticket)
    db.session.commit()

def db_update_ticket_from_form(ticket, form):
    if not isinstance(form, UpdateTicketForm):
        raise TypeError 

    ticket.title = form.title.data
    ticket.content = form.content.data
    ticket.street = form.street.data
    ticket.house_number = form.house_num.data

    ticket.images.clear()
    for form_image in form.picture.data:
        picture = save_picture(form_image)
        image = Image(url='/static/ticket_pics/' + picture)
        ticket.images.append(image)
        
    db.session.commit()

def db_delete_ticket(ticket):
    db.session.delete(ticket)
    db.session.commit()

def db_get_ticket_or_404(ticket_id):
    return Ticket.query.get_or_404(ticket_id)