from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from TownIssues import db, login_manager
from sqlalchemy.ext.hybrid import hybrid_property

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user_t'
    id = db.Column('id_user', db.Integer, primary_key=True)
    name = db.Column('firstname', db.String(50), nullable=False)
    surname = db.Column('surname', db.String(50), nullable=False)
    email = db.Column('email', db.String(254), nullable=False, unique=True)
    password = db.Column('password_hash', db.String(60), nullable=False)
    role = db.Column('u_role', db.Enum('admin', 'resident', 'manager', 'technician'), nullable=False)

    resident = db.relationship('Resident', uselist=False, cascade='all, delete-orphan', backref='user', lazy=True)
    manager = db.relationship('Manager', uselist=False, cascade='all, delete-orphan', backref='user', lazy=True)
    technician = db.relationship('Technician', uselist=False, cascade='all, delete-orphan', backref='user', lazy=True)

    @hybrid_property
    def fullname(self):
        return self.name + " " + self.surname

    def __repr__(self): #returns data
        return f"User('{self.name}', {self.surname}, {self.email})"
    

class Manager(db.Model):
    __tablename__ = 'manager'
    id = db.Column('id_manager', db.Integer, primary_key=True)
    phone_number = db.Column(db.String(50), nullable=True)

    id_user = db.Column(db.Integer, db.ForeignKey('user_t.id_user'), nullable=False)

    requests = db.relationship('ServiceRequest', cascade='all, delete-orphan', backref='manager', lazy=True)
    comments = db.relationship('TicketComment', cascade='all, delete-orphan', backref='author', lazy=True)

    def __repr__(self): #returns data
        return f"CityManager('{self.phone_number} {self.user}')"
    
 
class Technician(db.Model):
    __tablename__ = 'technician'
    id = db.Column('id_technician', db.Integer, primary_key=True)
    phone_number = db.Column(db.String(50), nullable=True)

    id_user = db.Column(db.Integer, db.ForeignKey('user_t.id_user'), nullable=False)

    requests = db.relationship('ServiceRequest', cascade='all, delete-orphan', backref='technician', lazy=True)
    comments = db.relationship('RequestComment', cascade='all, delete-orphan', backref='author', lazy=True)


    def __repr__(self): #returns data
        return f"ServiceTechnician('{self.phone_number} {self.user}')"
    
 
class Resident(db.Model):
    __tablename__ = 'resident'
    id = db.Column('id_resident', db.Integer, primary_key=True)

    id_user = db.Column(db.Integer, db.ForeignKey('user_t.id_user'), nullable=False)

    tickets = db.relationship('Ticket',  cascade='all, delete-orphan', backref='author', lazy=True)
    
    def __repr__(self): #returns data
        return f"Resident('{self.user}')"
    
class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column('id_ticket', db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    street = db.Column(db.String(200), nullable=False)
    house_number = db.Column(db.Integer, nullable=True)
    current_state = db.Column(db.String(200), nullable=False, default='Accepted')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    
    id_resident = db.Column(db.Integer, db.ForeignKey('resident.id_resident'), nullable=True)
    
    images = db.relationship('Image',  cascade='all, delete-orphan', backref='ticket', lazy=True)
    requests = db.relationship('ServiceRequest',  cascade='all, delete-orphan', backref='ticket', lazy=True, order_by='ServiceRequest.id.desc()')
    comments = db.relationship('TicketComment', order_by="desc(TicketComment.created_at)", cascade='all, delete-orphan', backref='ticket', lazy=True)

    def __repr__(self): #returns data
        return f"""Ticket('{self.title}, {self.content}, {self.street}, {self.house_number},
                {self.current_state}, {self.created_at}, {self.author}')"""


class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    id = db.Column('id_service_request', db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_finished = db.Column(db.Boolean, nullable=False, default=False)
    estimated_time = db.Column(db.TIMESTAMP, nullable=True)
    real_time = db.Column(db.Float, nullable=True)
    price = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

    id_manager = db.Column(db.Integer, db.ForeignKey('manager.id_manager'), nullable=False)
    id_technician = db.Column(db.Integer, db.ForeignKey('technician.id_technician'), nullable=True)
    id_ticket = db.Column(db.Integer, db.ForeignKey('ticket.id_ticket'), nullable=False)

    comments = db.relationship('RequestComment',  cascade='all, delete-orphan', backref='request', lazy=True, order_by='RequestComment.created_at.desc()')

     
    def __repr__(self): #returns data
        return f"""ServiceRequest('{self.content}, {self.is_finished}, {self.estimated_time},
         {self.real_time}, {self.price}, {self.created_at}, {self.manager}, {self.technician}, {self.ticket}')"""


class RequestComment(db.Model):
    __tablename__ = 'request_comment'
    id = db.Column('id_request_comment', db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

    id_service_request = db.Column(db.Integer, db.ForeignKey('service_request.id_service_request'), nullable=False)
    id_technician = db.Column(db.Integer, db.ForeignKey('technician.id_technician'), nullable=False)

    def __repr__(self): #returns data
        return f"RequestComment('{self.content}, {self.created_at}, {self.request}, {self.author}')"


class TicketComment(db.Model):
    __tablename__ = 'ticket_comment'
    id = db.Column('id_ticket_comment', db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

    id_ticket = db.Column(db.Integer, db.ForeignKey('ticket.id_ticket'), nullable=False)
    id_manager = db.Column(db.Integer, db.ForeignKey('manager.id_manager'), nullable=False)

    def __repr__(self): #returns data
        return f"RequestComment('{self.content}, {self.created_at}, {self.ticket}, {self.author}')"


class Image(db.Model):
    __tablename__ = 'attached_image'
    id = db.Column('id_image', db.Integer, primary_key=True)
    url = db.Column('url_path', db.Text, nullable=False)

    id_ticket = db.Column(db.Integer, db.ForeignKey('ticket.id_ticket'), nullable=False)
