from flask import Blueprint, render_template, request
from flask_login import login_required
from TownIssues.models import Ticket

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/tickets")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    tickets = Ticket.query.order_by(Ticket.datetime_created.desc()).paginate(page=page, per_page=5)
    return render_template('tickets.html', tickets=tickets)
