from pydoc import doc

from flask import current_app
from TownIssues import db
from flask_login import current_user
from TownIssues.models import Image, Ticket, ServiceRequirement
import os
from TownIssues.service_requirements.forms import AddRequirementForm, UpdateRequirementForm


def db_add_requirement_from_form(form):
    if not isinstance(form, AddRequirementForm):
        raise TypeError

    requirement = ServiceRequirement(content=form.content.data)
    db.session.add(requirement)
    db.session.commit()


def db_update_requirement_from_form(requirement, form):
    if not isinstance(form, UpdateRequirementForm):
        raise TypeError

    requirement.content = form.content.data
    requirement.estimated_time = form.estimated_time.data
    requirement.real_time = form.real_time.data
    requirement.price = form.price.data
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
