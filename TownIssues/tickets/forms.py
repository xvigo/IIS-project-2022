from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class AddTicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    house_num = IntegerField('House Number', validators=[DataRequired(), NumberRange(min=1, message="Please enter a valid house number.")])
    submit = SubmitField('Create Ticket')

class UpdateTicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    house_num = IntegerField('House Number', validators=[DataRequired(), NumberRange(min=1, message="Please enter a valid house number.")])
    submit = SubmitField('Update Ticket')

    def prefill(self, ticket):
        self.title.data = ticket.title
        self.content.data = ticket.content
        self.street.data = ticket.street
        self.house_num.data = ticket.house_number