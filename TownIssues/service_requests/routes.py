from flask import Blueprint, flash, abort, redirect, url_for, render_template, request
from flask_login import login_required, current_user

from TownIssues.service_requests.forms import AddRequestForm, RequestCommentForm, \
    RequestEditCommentForm, UpdateRequestForm
from TownIssues.models import ServiceRequest, RequestComment, Ticket
from TownIssues.service_requests import service
from TownIssues.users.utils import check_permissions, has_permissions, check_technician_permitted
from TownIssues.tickets import service as ticket_service

service_requests = Blueprint('service_requests', __name__)

@service_requests.route("/tickets/<int:ticket_id>/add_request", methods=['GET', 'POST'])
@login_required
def add_request(ticket_id):
    """Route for adding ticket service requests."""
    check_permissions(allowed_roles=['manager'])

    form = AddRequestForm()
    form.init_technicians()
    if form.validate_on_submit():
        ticket = ticket_service.get_ticket_or_404(ticket_id=ticket_id)
        ticket.current_state = "In process"
        request = ServiceRequest(manager=current_user.manager, id_ticket=ticket_id)
        form.populate_request(request=request)
        service.add_request(request=request)
        flash('Request created successfully.', 'success')
        return redirect(url_for('tickets.ticket_detail', ticket_id=ticket_id))

    return render_template('add_request.html', title='Add Request', form=form, legend='Create New Request')



@service_requests.route("/requests/<int:request_id>/update",
                            methods=['GET', 'POST'])
@login_required
def update_request(request_id):
    """Manager route for updating service request."""
    request = service.get_request_or_404(request_id)
    check_permissions(allowed_user=request.manager.user)

    form = AddRequestForm(submit_label='Update Request', technician=request.id_technician)
    form.init_technicians()

    if form.validate_on_submit():
        form.populate_request(request)
        service.update()
        flash('Request updated successfully.', 'success')
        return redirect(url_for('service_requests.request_detail', request_id=request.id))

    form.prefill(request)

    return render_template('add_request.html', title='Edit Request', form=form, legend='Edit Request')


@service_requests.route("/requests/<int:request_id>/update/technician",
                            methods=['GET', 'POST'])
@login_required
def update_request_as_technician(request_id):
    """Manager route for updating service request."""
    request = service.get_request_or_404(request_id)
    check_permissions(allowed_user=request.technician.user)

    form = UpdateRequestForm(submit_label='Update Request', technician=request.id_technician)

    if form.validate_on_submit():
        form.populate_request(request)
        service.update()
        flash('Request updated successfully.', 'success')
        return redirect(url_for('service_requests.request_detail', request_id=request.id))

    form.prefill(request)

    return render_template('update_request.html', title='Edit Request', form=form, legend='Edit Request')


@service_requests.route("/requests/<int:request_id>", methods=['GET', 'POST'])
@login_required
def request_detail(request_id):
    """Route for viewing service request details."""
    check_permissions(banned_roles=["resident"])
    request = service.get_request_or_404(request_id)
    check_technician_permitted(request.technician)

    add_comment_form = RequestCommentForm()
    edit_comment_form = RequestEditCommentForm()

    if add_comment_form.submitted_and_valid() and has_permissions(allowed_roles=['technician']):
        comment = RequestComment(request=request, id_technician=current_user.technician.id)
        add_comment_form.populate_comment(comment)
        service.add_request_comment(comment=comment)
        flash('Comment added successfully.', 'success')
        add_comment_form.clear()

    elif edit_comment_form.submitted_and_valid():
        comment = service.get_request_comment_or_404(edit_comment_form.edit_id.data)
        check_permissions(allowed_user=comment.author.user)
        edit_comment_form.populate_comment(comment)
        service.update()
        flash('Comment updated successfully.', 'success')

    return render_template('request_detail.html', request=request, has_permissions=has_permissions,
                           title='Update request', legend='Update request', add_comment_form=add_comment_form,
                           edit_comment_form=edit_comment_form)


@service_requests.route("/delete_ticket_request/<int:request_id>", methods=['POST'])
@login_required
def delete_request(request_id):
    """Route for deleting service request."""
    request = service.get_request_or_404(request_id=request_id)
    check_permissions(allowed_user=request.manager.user)
    ticket_id = request.ticket_id
    service.delete_request(request=request)
    return redirect(url_for("tickets.ticket_detail", ticket_id=ticket_id))

@service_requests.route("/delete_request_comment/<int:comment_id>", methods=['POST'])
@login_required
def delete_comment(comment_id):
    """Route for deleting request comment."""
    comment = service.get_request_comment(comment_id=comment_id)
    allowed = has_permissions(allowed_user=comment.author.user)
    
    if comment and allowed:
        service.delete_request_comment(comment=comment)
    return redirect(url_for('main.home'))

@service_requests.route("/my_service_requests_p", methods=['GET'])
@login_required
def my_requests_pending():
    """Route for deleting request comment."""
    check_permissions(allowed_roles=["technician"])

    page = request.args.get('page', 1, type=int)
    requests = service.get_requests_list(page=page, is_finished=False, technician=current_user.technician)
    
    return render_template('requests_list.html', requests=requests, title='Pending Service Requests')

@service_requests.route("/my_service_requests", methods=['GET'])
@login_required
def my_requests():
    """Route for deleting request comment."""
    check_permissions(allowed_roles=["technician"])

    page = request.args.get('page', 1, type=int)
    requests = service.get_requests_list(page=page, technician=current_user.technician)
    
    return render_template('requests_list.html', requests=requests, title='All Service Requests')