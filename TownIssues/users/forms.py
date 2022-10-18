from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from TownIssues.models import Technician, User, Resident, Manager
from flask_login import current_user
from TownIssues import bcrypt

class RegistrationForm(FlaskForm):              
    email = StringField('Email', validators=[DataRequired(), Email(message="Email address has invalid format.")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=50), EqualTo('confirm_password', message="Passwords do not match. Try again!")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=4, max=50)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=50)])   
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('User with this email address already exists. Please use a different one or log in.')

    def populate_resident_user(self, user):
        user.email = self.email.data
        user.password = bcrypt.generate_password_hash(self.password.data).decode('utf-8')
        user.name = self.name.data
        user.surname = self.surname.data
        user.resident = Resident()
        user.role = 'resident'



class LoginForm(FlaskForm):              
    email = StringField('Email', validators=[DataRequired(), Email(message="Email address has invalid format.")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=30)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class AccountDetailsForm(FlaskForm):              
    
    email = StringField('Email', validators=[DataRequired(), Email(message="Email address has invalid format.")])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=50)])   
    phone_number = StringField('Phone Number')   
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data == current_user.email or current_user.role == 'admin':
            return

        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('User with this email address already exists. Please use a different one.')

    def prefill(self, user):
        self.email.data = user.email
        self.name.data = user.name
        self.surname.data = user.surname

        if user.manager:
            self.phone_number.data = user.manager.phone_number
        elif user.technician:
            self.phone_number.data = user.technician.phone_number
    
    def populate_user(self, user):
        user.email = self.email.data
        user.name = self.name.data
        user.surname = self.surname.data

        if user.manager:
            user.manager.phone_number = self.phone_number.data
        elif user.technician:
            user.technician.phone_number = self.phone_number.data
            
class UserDetailForm(FlaskForm):              
    
    email = StringField('Email', validators=[DataRequired(), Email(message="Email address has invalid format.")])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=50)])   
    phone_number = StringField('Phone Number')   
    submit = SubmitField('Update')

    def prefill(self, user):
        self.email.data = user.email
        self.name.data = user.name
        self.surname.data = user.surname

        if user.manager:
            self.phone_number.data = user.manager.phone_number
        elif user.technician:
            self.phone_number.data = user.technician.phone_number
    
    def populate_user(self, user):
        user.email = self.email.data
        user.name = self.name.data
        user.surname = self.surname.data

        if user.manager:
            user.manager.phone_number = self.phone_number.data
        elif user.technician:
            user.technician.phone_number = self.phone_number.data


class AddUserForm(FlaskForm):              
    email = StringField('Email', validators=[DataRequired(), Email(message="Email address has invalid format.")])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=50)])  
    role = SelectField(u'Role', choices=[('manager', 'Town Manager'), ('technician', 'Service Technician'), ('resident', 'Town Resident'), ('admin', 'Administrator')]) 
    phone_number = StringField('Phone Number')   
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=50), EqualTo('confirm_password', message="Passwords do not match. Try again!")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=4, max=50)])
    submit = SubmitField('Add User')

    def populate_user(self, user):
        user.email = self.email.data
        user.password = bcrypt.generate_password_hash(self.password.data).decode('utf-8')
        user.name = self.name.data
        user.surname = self.surname.data
        user.role = self.role.data

        if user.role == 'resident':
            user.resident = Resident()
        elif user.role == 'manager':
            user.manager = Manager(phone_number=self.phone_number.data)
        elif user.role == 'technician':
            user.technician = Technician(phone_number=self.phone_number.data)


class ChangePasswordForm(FlaskForm):              
    
    current_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=4, max=50)])

    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=4, max=50), EqualTo('confirm_new_password', message="Passwords do not match. Try again!")])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), Length(min=4, max=50)]) 

    submit = SubmitField('Change Password')


class AddTechnicianForm(FlaskForm):              
    email = StringField('Email', validators=[DataRequired(), Email(message="Email address has invalid format.")])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=50)])  
    phone_number = StringField('Phone Number')   
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=50), EqualTo('confirm_password', message="Passwords do not match. Try again!")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=4, max=50)])
    submit = SubmitField('Add Technician')

    def populate_user(self, user):
        user.email = self.email.data
        user.password = bcrypt.generate_password_hash(self.password.data).decode('utf-8')
        user.name = self.name.data
        user.surname = self.surname.data
        user.role = "technician"
        user.technician = Technician(phone_number=self.phone_number.data)
