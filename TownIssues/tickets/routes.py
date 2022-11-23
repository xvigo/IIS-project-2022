from flask import Blueprint, flash, redirect, url_for, render_template, abort, request
from flask_login import login_required, current_user
from TownIssues.tickets.forms import AddTicketForm, AddCommentForm, EditCommentForm, UpdateTicketForm
from TownIssues.models import Ticket, TicketComment
from TownIssues.users.utils import check_permissions, has_permissions
from TownIssues.tickets import service
tickets = Blueprint('tickets', __name__)

@tickets.route("/tickets/add", methods=['GET', 'POST'])
@login_required
def add_ticket():
    """Resident route for adding new tickets."""
    check_permissions(allowed_roles=['resident'])

    form = AddTicketForm()
    if form.validate_on_submit():
        ticket = Ticket(author=current_user.resident)
        form.populate_ticket(ticket=ticket)
        service.add_ticket(ticket=ticket)
        flash('Ticked created successfully.', 'success')
        return redirect(url_for('tickets.tickets_list'))

    return render_template('add_ticket.html', title='Account', form=form, legend='Create New Ticket')


@tickets.route("/tickets/<int:ticket_id>", methods=['GET', 'POST'])
@login_required
def ticket_detail(ticket_id):
    """Route for displaying ticket details."""
    ticket = service.get_ticket_or_404(ticket_id=ticket_id)
    add_comment_form = AddCommentForm()
    edit_comment_form = EditCommentForm()


    if add_comment_form.submitted_and_valid() and has_permissions(allowed_roles='manager'):
        comment = TicketComment(ticket=ticket, author=current_user.manager)
        add_comment_form.populate_comment(comment=comment)
        service.add_ticket_comment(comment=comment)
        flash('Comment added successfully.', 'success')
        add_comment_form.clear()

    elif edit_comment_form.submitted_and_valid():
        comment = service.get_ticket_comment_or_404(edit_comment_form.edit_id.data)
        check_permissions(allowed_user=comment.author.user)
        edit_comment_form.populate_comment(comment)
        service.update()
        flash('Comment updated successfully.', 'success')

    return render_template('ticket_detail.html', title='Account', ticket=ticket, has_permissions=has_permissions,
                           add_comment_form=add_comment_form, edit_comment_form=edit_comment_form,
                           legend='Ticket Details')


@tickets.route("/tickets/<int:ticket_id>/update", methods=['GET', 'POST'])
@login_required
def update_ticket(ticket_id):
    """Route for updating ticket details."""
    ticket =service.get_ticket_or_404(ticket_id=ticket_id)
    check_permissions(allowed_user=ticket.author.user)

    form = UpdateTicketForm()
    if request.method == 'GET':
        form.prefill(ticket)

    elif form.validate_on_submit():
        form.populate_ticket(ticket=ticket)
        service.update()
        flash('Ticket updated successfully.', 'success')
        return redirect(url_for('tickets.ticket_detail', ticket_id=ticket.id))

    return render_template('update_ticket.html', title='Account', ticket=ticket, form=form, legend='Update Ticket')

@tickets.route("/tickets/<int:ticket_id>/finish", methods=['GET'])
@login_required
def finish_ticket(ticket_id):
    """Route for updating ticket details."""
    ticket =service.get_ticket_or_404(ticket_id=ticket_id)
    check_permissions(allowed_roles=['manager'])

    ticket.current_state = "Finished"
    service.update()
    flash('Ticket state updated successfully.', 'success')

    return redirect(url_for('tickets.ticket_detail', ticket_id=ticket.id))

@tickets.route("/tickets/<int:ticket_id>/deny", methods=['GET'])
@login_required
def deny_ticket(ticket_id):
    """Route for updating ticket details."""
    ticket =service.get_ticket_or_404(ticket_id=ticket_id)
    check_permissions(allowed_roles=['manager'])

    ticket.current_state = "Denied"
    service.update()
    flash('Ticket state updated successfully.', 'success')

    return redirect(url_for('tickets.ticket_detail', ticket_id=ticket.id))


@tickets.route("/tickets/<int:ticket_id>/delete", methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    """Route for deleting tickets."""
    ticket = service.get_ticket_or_404(ticket_id=ticket_id)
    check_permissions(allowed_roles=['resident', 'admin'], allowed_user=ticket.author.user)

    service.delete_ticket(ticket)
    flash('Ticket has been deleted successfully!', 'success')
    return redirect(url_for('main.home'))


@tickets.route("/tickets")
@login_required
def tickets_list():
    """Route vor viewing all tickets."""
    check_permissions(banned_roles=['technician'])
    page = request.args.get('page', 1, type=int)
    tickets = service.get_tickets_list(page=page)
    return render_template('tickets_list.html', tickets=tickets)


@tickets.route("/my_tickets")
@login_required
def my_tickets_list():
    """Route for viewing all tickets that current user created."""
    check_permissions(allowed_roles=['resident'])
    page = request.args.get('page', 1, type=int)
    tickets = service.get_tickets_list(page=page, author=current_user.resident)
    return render_template('tickets_list.html', tickets=tickets)


@tickets.route("/delete_ticket_comment/<int:comment_id>", methods=['POST'])
@login_required
def delete_comment(comment_id):
    """Route for deleting ticket comments."""
    comment = service.get_ticket_comment(comment_id=comment_id)
    allowed = has_permissions(allowed_user=comment.author.user)

    if comment and allowed:
        service.delete_ticket_comment(comment=comment)
    return redirect(url_for('main.home'))


@tickets.route("/delete_ticket_image/<int:image_id>", methods=['POST'])
@login_required
def delete_image(image_id):
    """Route for deleting ticket images."""
    image = service.get_ticket_image(image_id=image_id)
    allowed = has_permissions(allowed_user=image.ticket.author.user)
    
    if image and allowed:
        service.delete_ticket_image(image=image)
    return redirect(url_for('main.home'))


@tickets.route("/delete_orphan_images")
def delete_orphans():
    """Development route for deleting orphan image files
    caused by removing images directly from db."""
    from TownIssues.tickets.utils import delete_orphan_images
    delete_orphan_images()
    return render_template('layout.html')
 
