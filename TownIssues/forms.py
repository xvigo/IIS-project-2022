from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):              
    
    email = StringField('Email', validators=[DataRequired(), Email(message="Email address has invalid format.")])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=30), EqualTo('confirm_password', message="Passwords do not match. Try again!")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=4, max=30)])

    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=4, max=20)])   

    submit = SubmitField('Sign Up')



class LoginForm(FlaskForm):              
    
    email = StringField('Email', validators=[DataRequired(), Email(message="Email address has invalid format.")])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=30)])

    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Log In')