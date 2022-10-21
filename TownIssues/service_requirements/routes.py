from flask import Blueprint, flash, jsonify, redirect, url_for, render_template, abort, request
from flask_login import login_required, current_user

from TownIssues.service_requirements.forms import AddRequirementForm, UpdateRequirementForm, RequirementCommentForm, \
    RequirementEditCommentForm
from TownIssues.models import Ticket, ServiceRequirement, Technician, RequirementComment
from TownIssues import db
from TownIssues.service_requirements.repository import db_add_requirement_from_form, db_update_requirement_from_form, \
    db_delete_requirement
from TownIssues.users.utils import check_permissions, has_permissions

service_requirements = Blueprint('service_requirements', __name__)


# Add requirement
@service_requirements.route("/tickets/<int:ticket_id>/add_requirement", methods=['GET', 'POST'])
@login_required
def add_requirement(ticket_id):
    check_permissions(allowed_roles=['manager'])

    form = AddRequirementForm()
    technicians = Technician.query.all()
    # Now forming the list of tuples for SelectField
    technicians_names = [(technician.id, technician.user.fullname) for technician in technicians]
    form.technician.choices = technicians_names
    if form.validate_on_submit():
        requirement = ServiceRequirement(content=form.content.data, manager=current_user.manager,
                                         id_technician=form.technician.data, id_ticket=ticket_id)
        db.session.add(requirement)
        db.session.commit()
        flash('Requirement created successfully.', 'success')
        return redirect(url_for('tickets.ticket_detail', ticket_id=ticket_id))

    return render_template('add_requirement.html', title='Add requirement', form=form, legend='Create New Requirement')


# Requirement detail
@service_requirements.route("/tickets/<int:ticket_id>/requirements/<int:requirement_id>", methods=['GET', 'POST'])
@login_required
def requirement_detail(requirement_id, ticket_id):
    add_comment_form = RequirementCommentForm()
    edit_comment_form = RequirementEditCommentForm()
    requirement = ServiceRequirement.query.get_or_404(requirement_id)
    ticket = Ticket.query.get_or_404(ticket_id)

    if request.method == 'POST' and add_comment_form.validate_on_submit() and current_user.role in ['admin',
                                                                                                    'technician',
                                                                                                    'manager']:  # TODO zmenit na technicain

        comment = RequirementComment(content=add_comment_form.content.data, requirement=requirement,
                                     id_technician=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added succesfully.', 'success')

    elif request.method == 'POST' and edit_comment_form.validate_on_submit():
        comment = RequirementComment.query.get_or_404(edit_comment_form.edit_id.data)
        comment.content = edit_comment_form.edit_content.data
        db.session.commit()
        flash('Comment updated succesfully.', 'success')

    return render_template('requirement_detail.html', requirement=requirement, has_permissions=has_permissions,
                           title='Update requirement', legend='Update requirement', add_comment_form=add_comment_form,
                           edit_comment_form=edit_comment_form, ticket=ticket)


# Update requirement
@service_requirements.route("/tickets/<int:ticket_id>/requirements/<int:requirement_id>/update",
                            methods=['GET', 'POST'])
@login_required
def update_requirement(requirement_id, ticket_id):
    requirement = ServiceRequirement.query.get_or_404(requirement_id)
    ticket = Ticket.query.get_or_404(ticket_id)
    check_permissions(allowed_roles=['manager', 'admin'])  # TODO Zmenit na technician (asi)

    form = UpdateRequirementForm()
    if request.method == 'GET':
        form.prefill(requirement)

    elif form.validate_on_submit():
        db_update_requirement_from_form(requirement, form)
        flash('Requirement updated successfully.', 'success')
        return redirect(url_for('tickets.ticket_detail'))

    return render_template('update_requirement.html', title='Update Requirement', requirement=requirement, ticket=ticket,
                           form=form, legend='Update Requirement')


@service_requirements.route("/delete_requirement_comment/<int:comment_id>",
                            methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = RequirementComment.query.get_or_404(comment_id)
    check_permissions(allowed_roles=['manager', 'technician', 'admin'])
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("tickets.tickets_list"))


@service_requirements.route("/delete_ticket_requirement/<int:requirement_id>",
                            methods=['POST'])
@login_required
def delete_requirement(requirement_id):
    requirement = ServiceRequirement.query.get_or_404(requirement_id)
    check_permissions(allowed_roles=['manager', 'technician', 'admin'])
    db.session.delete(requirement)
    db.session.commit()
    return redirect(url_for("tickets.tickets_list"))
