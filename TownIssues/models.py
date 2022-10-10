from datetime import datetime
from flask_login import UserMixin
from TownIssues import db, login_manager

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	__tablename__ = 'u_user'
	id = db.Column('id_user', db.Integer, primary_key=True)
	name = db.Column('u_name', db.String(50), nullable=False)
	surname = db.Column('u_surname', db.String(50), nullable=False)
	email = db.Column('u_email', db.String(254), unique=True, nullable=False)
	password = db.Column('u_password', db.String(60), nullable=False)

	# Queries
	tickets = db.relationship('Ticket', backref='author', lazy=True)
	# relationship TODO generalization
	
	def __repr__(self): #returns data
		return f"User('{self.name}', {self.surname}, {self.email})"
	

class Ticket(db.Model):
	__tablename__ = 'ticket'
	id = db.Column('id_ticket', db.Integer, primary_key=True)
	name = db.Column('t_name', db.String(50), nullable=False)
	description = db.Column('t_description', db.Text, nullable=False)
	street = db.Column(db.Text, nullable=False)
	house_number = db.Column(db.Integer, nullable=False)
	state = db.Column('t_state', db.Text, nullable=False)
	datetime_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	# FK
	id_resident = db.Column(db.Integer, db.ForeignKey('u_user.id_user'), nullable=False)
	# relationship
	#service_requirements = db.relationship('ServiceRequirement', backref='belong_to', lazy=True)
	#ticket_comments = db.relationship('TicketComment', backref='belong_to', lazy=True)
	#images = db.relationship('Image', backref='belong_to', lazy=True)
	
	def __repr__(self): #returns data
		return f"Ticket('{self.name}, {self.description}, {self.street}, {self.house_number}, {self.state}')"
	
 

# class CityManager(db.Model):
# 	__tablename__ = 'city_manager'
# 	id = db.Column('id_city_manager', db.Integer, primary_key=True)
# 	phone_number = db.Column(db.String(20), nullable=False)
#  	# relationship
# 	#technicians_created = db.relationship('ServiceTechnician', backref='created_by', lazy=True)
# 	s_requirements_created = db.relationship('Requirement', backref='created_by', lazy=True)
# 	tic_comments_listed = db.relationship('TicketComment', backref='listed_by', lazy=True)
	
# 	def __repr__(self): #returns data
# 		return f"CityManager('{self.phone_number}')"
	
 
# class ServiceTechnician(db.Model):
# 	__tablename__ = 'service_technician'
# 	id = db.Column('id_service_technician', db.Integer, primary_key=True)
# 	phone_number = db.Column(db.String(20), nullable=False)
# 	# FK
# 	id_manager = db.Column(db.Integer, db.ForeignKey('citymanager.id'), nullable=False)
# 	# relationship
# 	requirements_handled = db.relationship('ServiceRequirement', backref='handled_by', lazy=True)
# 	req_comments_listed = db.relationship('RequirementComment', backref='listed_by', lazy=True)
	
# 	def __repr__(self): #returns data
# 		return f"ServiceTechnician('{self.phone_number}')"
	
 
# class Resident(db.Model):
# 	__tablename__ = 'resident'
# 	id = db.Column('id_resident', db.Integer, primary_key=True)
# 	# relationship
# 	tickets_created = db.relationship('Ticket', backref='created_by', lazy=True)
	
	

# class ServiceRequirement(db.Model):
# 	__tablename__ = 'service_requirement'
# 	id = db.Column('id_service_requirement', db.Integer, primary_key=True)
# 	description = db.Column('r_description', db.Text, nullable=False)
# 	state = db.Column('r_state', db.Text, nullable=False)
# 	estimated_time = db.Column(db.DateTime, nullable=False)
# 	price = db.Column(db.Integer, nullable=False)
# 	real_time = db.Column(db.DateTime, nullable=False)
# 	# FK
# 	id_manager = db.Column(db.Integer, db.ForeignKey('citymanager.id'), nullable=False)
# 	id_technician = db.Column(db.Integer, db.ForeignKey('servicetechnician.id'), nullable=False)
# 	id_ticket = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
# 	# relationship
# 	requirement_comments = db.relationship('RequirementComment', backref='belong_to', lazy=True)
 
# 	def __repr__(self): #returns data
# 		return f"ServiceRequirement('{self.description}, {self.state}, {self.estimated_time}, {self.price}, {self.real_time}')"


# class RequirementComment(db.Model):
# 	__tablename__ = 'requirement_comment'
# 	id = db.Column('id_requirement_comment', db.Integer, primary_key=True)
# 	date = db.Column('rc_date', db.DateTime, nullable=False)
# 	text = db.Column('rc_text', db.Text, nullable=False)
# 	# FK
# 	id_requirement = db.Column('id_service_requirement', db.Integer, db.ForeignKey('servicerequirement.id'), nullable=False)
# 	id_technician = db.Column('id_service_technician', db.Integer, db.ForeignKey('servicetechnician.id'), nullable=False)

# 	def __repr__(self): #returns data
# 		return f"RequirementComment('{self.date}, {self.text}')"


# class TicketComment(db.Model):
# 	__tablename__ = 'ticket_comment'
# 	id = db.Column('id_ticket_comment', db.Integer, primary_key=True)
# 	date = db.Column('tc_date', db.DateTime, nullable=False)
# 	text = db.Column('tc_text', db.Text, nullable=False)
# 	# FK
# 	id_manager = db.Column('id_city_manager', db.Integer, db.ForeignKey('citymanager.id'), nullable=False)
# 	id_ticket = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
 
# 	def __repr__(self): #returns data
# 		return f"TicketComment('{self.date}, {self.text}')"


class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column('id_image', db.Integer, primary_key=True)
    name = db.Column('i_name', db.String(50), nullable=False)
    data = db.Column('i_date', db.String(20), nullable=False) #use hash
    # FK
    id_ticket = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)