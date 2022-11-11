from flask import Blueprint, redirect, url_for, abort
from flask_login import login_required, current_user
from TownIssues.models import Ticket

main = Blueprint('main', __name__)

@main.route("/")
@login_required
def home():
    if current_user.role == 'admin':
        return redirect(url_for('users.users_list'))
    elif current_user.role == 'resident':
        return redirect(url_for('tickets.tickets_list'))
    elif current_user.role == 'manager':
        return redirect(url_for('tickets.tickets_list'))
    elif current_user.role == 'technician':
        return redirect(url_for('service_requirements.my_requirements'))
    else:
        abort(404)
    return