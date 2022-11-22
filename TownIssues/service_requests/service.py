from TownIssues import db
from TownIssues.models import ServiceRequest, RequestComment


def add_request(request):
    """Add service request to database."""
    db.session.add(request)
    db.session.commit()

def get_request_or_404(request_id):
    """Return request with given id or displays 404 page."""
    return ServiceRequest.query.get_or_404(request_id)

def add_request_comment(comment):
    """Add service request comment to database."""
    db.session.add(comment)
    db.session.commit()

def delete_request(request):
    """Delete request from database."""
    db.session.delete(request)
    db.session.commit()

def get_request_comment(comment_id):
    """Return request comment with given id."""
    return RequestComment.query.get_or_404(comment_id)

def get_request_comment_or_404(comment_id):
    """Return request comment with given id or displays 404 page."""
    return RequestComment.query.get_or_404(comment_id)

def delete_request_comment(comment):
    """Delete request comment from database."""
    db.session.delete(comment)
    db.session.commit()

def get_requests_list(page, order=ServiceRequest.created_at.desc(), amount=100, technician=None):
    """Returns <amount> tickets with given author from given page in given order."""
    if technician is not None:
        return ServiceRequest.query.filter_by(technician=technician).order_by(order).paginate(page=page, per_page=amount)
    else:
        return ServiceRequest.query.order_by(order).paginate(page=page, per_page=amount)


def update():
    """Saves any changes made in models to db."""
    db.session.commit()
