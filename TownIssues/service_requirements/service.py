from TownIssues import db
from TownIssues.models import ServiceRequirement, RequirementComment


def add_requirement(requirement):
    """Add service requirement to database."""
    db.session.add(requirement)
    db.session.commit()

def get_requirement_or_404(requirement_id):
    """Return requirement with given id or displays 404 page."""
    return ServiceRequirement.query.get_or_404(requirement_id)

def add_requirement_comment(comment):
    """Add service requirement comment to database."""
    db.session.add(comment)
    db.session.commit()

def delete_requirement(requirement):
    """Delete requirement from database."""
    db.session.delete(requirement)
    db.session.commit()

def get_requirement_comment(comment_id):
    """Return requirement comment with given id."""
    return RequirementComment.query.get_or_404(comment_id)

def get_requirement_comment_or_404(comment_id):
    """Return requirement comment with given id or displays 404 page."""
    return RequirementComment.query.get_or_404(comment_id)

def delete_requirement_comment(comment):
    """Delete requirement comment from database."""
    db.session.delete(comment)
    db.session.commit()

def get_requirements_list(page, order=ServiceRequirement.created_at.desc(), amount=100, technician=None):
    """Returns <amount> tickets with given author from given page in given order."""
    if technician is not None:
        return ServiceRequirement.query.filter_by(technician=technician).order_by(order).paginate(page=page, per_page=amount)
    else:
        return ServiceRequirement.query.order_by(order).paginate(page=page, per_page=amount)


def update():
    """Saves any changes made in models to db."""
    db.session.commit()
