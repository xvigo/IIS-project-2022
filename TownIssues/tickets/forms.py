from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class AddTicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    house_num = IntegerField('House Number', validators=[DataRequired(), NumberRange(min=1, message="Please enter a valid house number.")])
    submit = SubmitField('Create Ticket')
    picture = FileField('Choose picture', validators=[FileAllowed(['jpg', 'png'])])

class UpdateTicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    house_num = IntegerField('House Number', validators=[DataRequired(), NumberRange(min=1, message="Please enter a valid house number.")])
    submit = SubmitField('Update Ticket')
    picture = FileField('Choose picture', validators=[FileAllowed(['jpg', 'png'])])