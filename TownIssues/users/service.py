from TownIssues import db
from TownIssues.models import User
from TownIssues.tickets.utils import delete_images_from_tickets


def add_user(user):
    """Adds user into database."""
    db.session.add(user)
    db.session.commit()


def get_user(email):
    """Returns first user in database with given email."""
    return User.query.filter_by(email=email).first()


def get_user_or_404(user_id):
    """Return user with given id or displays 404 page."""
    return User.query.get_or_404(user_id)


def get_users_list(page, order=User.id.desc(), amount=100, role=None):
    """Returns <amount> users with given role from given page in given order."""
    if role is not None:
        return User.query.filter_by(role=role).order_by(order).paginate(page=page, per_page=amount)
    else:
        return User.query.order_by(order).paginate(page=page, per_page=amount)


def delete_user(user):
    """Deletes user from database."""
    if user.role == 'resident':
        # delete images from filesystem before tickets are cascade deleted
        delete_images_from_tickets(user.resident.tickets)

    db.session.delete(user)
    db.session.commit()


def update():
    """Saves any changes made in models to db."""
    db.session.commit()