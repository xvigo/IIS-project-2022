from TownIssues import db
from TownIssues.models import Ticket, TicketComment
from TownIssues.tickets.utils import delete_images_from_tickets

def add_ticket(ticket):
    """Adds ticket into database."""
    db.session.add(ticket)
    db.session.commit()


def get_ticket_or_404(ticket_id):
    """Return ticket with given id or displays 404 page."""
    return Ticket.query.get_or_404(ticket_id)


def delete_ticket(ticket):
    """Delete ticket from database and its images from filesystem."""
    delete_images_from_tickets(tickets=[ticket])
    db.session.delete(ticket)
    db.session.commit()


def get_tickets_list(page, order=Ticket.created_at.desc(), amount=100, author=None):
    """Returns <amount> tickets with given author from given page in given order."""
    if author is not None:
        return Ticket.query.filter_by(author=author).order_by(order).paginate(page=page, per_page=amount)
    else:
        return Ticket.query.order_by(order).paginate(page=page, per_page=amount)

def add_ticket_comment(comment):
    """Adds ticket into database."""
    db.session.add(comment)
    db.session.commit()

def get_ticket_comment_or_404(comment_id):
    """Return ticket comment with given id or displays 404 page."""
    return TicketComment.query.get_or_404(comment_id)

def get_ticket_comment(comment_id):
    """Return ticket comment with given id."""
    return TicketComment.query.get_or_404(comment_id)

def delete_ticket_comment(comment):
    """Delete ticket comment from database."""
    db.session.delete(comment)
    db.session.commit()

def update():
    """Saves any changes made in models to db."""
    db.session.commit()
