from flask import Blueprint, flash, abort, redirect, url_for, render_template, request
from flask_login import login_required, current_user

from TownIssues.service_requirements.forms import AddRequirementForm, RequirementCommentForm, \
    RequirementEditCommentForm, UpdateRequirementForm
from TownIssues.models import ServiceRequirement, RequirementComment
from TownIssues.service_requirements import service
from TownIssues.users.utils import check_permissions, has_permissions, check_technician_permitted
from TownIssues.tickets import service as ticket_service

service_requirements = Blueprint('service_requirements', __name__)

@service_requirements.route("/tickets/<int:ticket_id>/add_requirement", methods=['GET', 'POST'])
@login_required
def add_requirement(ticket_id):
    """Route for adding ticket service requirements."""
    check_permissions(allowed_roles=['manager'])

    form = AddRequirementForm()
    form.init_technicians()
    if form.validate_on_submit():
        requirement = ServiceRequirement(manager=current_user.manager, id_ticket=ticket_id)
        form.populate_requirement(requirement=requirement)
        service.add_requirement(requirement=requirement)
        flash('Requirement created successfully.', 'success')
        return redirect(url_for('tickets.ticket_detail', ticket_id=ticket_id))

    return render_template('add_requirement.html', title='Add Requirement', form=form, legend='Create New Requirement')



@service_requirements.route("/requirements/<int:requirement_id>/update",
                            methods=['GET', 'POST'])
@login_required
def update_requirement(requirement_id):
    """Manager route for updating service requirement."""
    requirement = service.get_requirement_or_404(requirement_id)
    check_permissions(allowed_user=requirement.manager.user)

    form = AddRequirementForm(submit_label='Update Requirement', technician=requirement.id_technician)
    form.init_technicians()

    if form.validate_on_submit():
        form.populate_requirement(requirement)
        service.update()
        flash('Requirement updated successfully.', 'success')
        return redirect(url_for('service_requirements.requirement_detail', requirement_id=requirement.id))

    form.prefill(requirement)

    return render_template('add_requirement.html', title='Edit Requirement', form=form, legend='Edit Requirement')


@service_requirements.route("/requirements/<int:requirement_id>/update/technician",
                            methods=['GET', 'POST'])
@login_required
def update_requirement_as_technician(requirement_id):
    """Manager route for updating service requirement."""
    requirement = service.get_requirement_or_404(requirement_id)
    check_permissions(allowed_user=requirement.technician.user)

    form = UpdateRequirementForm(submit_label='Update Requirement', technician=requirement.id_technician)

    if form.validate_on_submit():
        form.populate_requirement(requirement)
        service.update()
        flash('Requirement updated successfully.', 'success')
        return redirect(url_for('service_requirements.requirement_detail', requirement_id=requirement.id))

    form.prefill(requirement)

    return render_template('update_requirement.html', title='Edit Requirement', form=form, legend='Edit Requirement')





@service_requirements.route("/requirements/<int:requirement_id>", methods=['GET', 'POST'])
@login_required
def requirement_detail(requirement_id):
    """Route for viewing service requirement details."""
    check_permissions(banned_roles=["resident"])
    requirement = service.get_requirement_or_404(requirement_id)
    check_technician_permitted(requirement.technician)

    add_comment_form = RequirementCommentForm()
    edit_comment_form = RequirementEditCommentForm()

    if add_comment_form.submitted_and_valid() and has_permissions(allowed_roles=['technician']):
        comment = RequirementComment(requirement=requirement, id_technician=current_user.technician.id)
        add_comment_form.populate_comment(comment)
        service.add_requirement_comment(comment=comment)
        flash('Comment added successfully.', 'success')
        add_comment_form.clear()

    elif edit_comment_form.submitted_and_valid():
        comment = service.get_requirement_comment_or_404(edit_comment_form.edit_id.data)
        check_permissions(allowed_user=comment.author.user)
        edit_comment_form.populate_comment(comment)
        service.update()
        flash('Comment updated successfully.', 'success')

    return render_template('requirement_detail.html', requirement=requirement, has_permissions=has_permissions,
                           title='Update requirement', legend='Update requirement', add_comment_form=add_comment_form,
                           edit_comment_form=edit_comment_form)


@service_requirements.route("/delete_ticket_requirement/<int:requirement_id>", methods=['POST'])
@login_required
def delete_requirement(requirement_id):
    """Route for deleting service requirement."""
    requirement = service.get_requirement_or_404(requirement_id=requirement_id)
    check_permissions(allowed_user=requirement.manager.user)
    ticket_id = requirement.ticket_id
    service.delete_requirement(requirement=requirement)
    return redirect(url_for("tickets.ticket_detail", ticket_id=ticket_id))

@service_requirements.route("/delete_requirement_comment/<int:comment_id>", methods=['POST'])
@login_required
def delete_comment(comment_id):
    """Route for deleting requirement comment."""
    comment = service.get_requirement_comment(comment_id=comment_id)
    allowed = has_permissions(allowed_user=comment.author.user)
    
    if comment and allowed:
        service.delete_requirement_comment(comment=comment)
    return redirect(url_for('main.home'))

@service_requirements.route("/my_service_requirements", methods=['GET'])
@login_required
def my_requirements():
    """Route for deleting requirement comment."""
    check_permissions(allowed_roles=["technician"])

    page = request.args.get('page', 1, type=int)
    requirements = service.get_requirements_list(page=page, technician=current_user.technician)
    
    return render_template('requirements_list.html', requirements=requirements, title='My Requirements')

# @service_requirements.route("/tickets/<int:ticket_id>/requirements/<int:requirement_id>/update",
#                             methods=['GET', 'POST'])
# @login_required
# def update_requirement(requirement_id, ticket_id):
#     """Manager route for updating service requirement."""
#     requirement = service.get_requirement_or_404(requirement_id)
#     check_permissions(allowed_user=requirement.manager.user)

#     ticket = ticket_service.get_ticket_or_404(ticket_id)

#     form = AddRequirementForm(submit_label='Update Requirement')
#     if request.method == 'GET':
#         form.prefill(requirement)

#     elif form.validate_on_submit():
#         form.populate_requirement(requirement)
#         service.update()
#         flash('Requirement updated successfully.', 'success')
#         return redirect(url_for('service_requirements.requirement_detail', ticket_id=ticket.id, requirement_id=requirement.id))

#     return render_template('update_requirement.html', title='Update Requirement', requirement=requirement, ticket=ticket,
#                            form=form, legend='Update Requirement')