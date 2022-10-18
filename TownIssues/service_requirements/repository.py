from pydoc import doc

from flask import current_app
from TownIssues import db
from flask_login import current_user
from TownIssues.models import Image, Ticket, ServiceRequirement
import os
from TownIssues.service_requirements.forms import AddRequirementForm


def db_add_requirement_from_form(form):
    if not isinstance(form, AddRequirementForm):
        raise TypeError

    requirement = ServiceRequirement(content=form.content.data)
    db.session.add(requirement)
    db.session.commit()


def db_update_ticket_from_form(ticket, form):
    if not isinstance(form, UpdateTicketForm):
        raise TypeError

    ticket.title = form.title.data
    ticket.content = form.content.data
    ticket.street = form.street.data
    ticket.house_number = form.house_num.data

    for image in ticket.images:
        path = 'TownIssues' + image.url
        if os.path.exists(path):
            os.remove(path)

    ticket.images.clear()
    for form_image in form.picture.data:
        if form_image.filename:
            picture = save_picture(form_image)
            image = Image(url='/static/ticket_pics/' + picture)
            ticket.images.append(image)

    db.session.commit()


def db_delete_ticket(ticket):
    # Delete ticket images from file system
    for image in ticket.images:
        path = 'TownIssues' + image.url
        if os.path.exists(path):
            os.remove(path)

    db.session.delete(ticket)
    db.session.commit()


def db_get_ticket_or_404(ticket_id):
    return Ticket.query.get_or_404(ticket_id)
