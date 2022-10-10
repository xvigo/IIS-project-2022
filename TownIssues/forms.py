from TownIssues import bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, MultipleFileField,PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from TownIssues.models import User
from flask_login import current_user

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

class LoginForm(FlaskForm):              
    
    email = StringField('Email', validators=[DataRequired(), Email(message="Email address has invalid format.")])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=30)])

    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Log In')

class UpdateAccountForm(FlaskForm):              
    
    email = StringField('Email', validators=[DataRequired(), Email(message="Email address has invalid format.")])

    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=50)])   

    submit = SubmitField('Update')
    def validate_email(self, email):
        if email.data == current_user.email:
            return
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('User with this email address already exists. Please use a different one.')


class ChangePasswordForm(FlaskForm):              
    
    current_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=4, max=50)])

    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=4, max=50), EqualTo('confirm_new_password', message="Passwords do not match. Try again!")])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), Length(min=4, max=50)]) 

    submit = SubmitField('Change Password')