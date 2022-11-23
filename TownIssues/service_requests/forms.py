from time import strftime

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField, BooleanField, DateField, \
    TimeField, FloatField, validators
from wtforms.validators import DataRequired, NumberRange, ValidationError
from flask_wtf.file import FileField, FileAllowed
from datetime import datetime
from TownIssues.models import Technician

def validate_estimated_time(form, field):
    if field.data and field.data < datetime.date(datetime.today()):
        raise ValidationError('Estimated time cannot be in past')

class AddRequestForm(FlaskForm):
    """Form for adding service request."""

    def __init__(self, submit_label = None, **kw):
        super(AddRequestForm, self).__init__(**kw)
        if submit_label is not None:
            self.submit.label.text = submit_label

    content = TextAreaField('Description', validators=[DataRequired()])
    technician = SelectField('Technician', validators=[DataRequired()])
    submit = SubmitField('Create Request')

    def init_technicians(self):
        """Add technicians to form select field."""
        technicians = Technician.query.all()
        technicians_names = [(technician.id, technician.user.fullname) for technician in technicians]
        self.technician.choices = technicians_names

    def populate_request(self, request):
        """Populates request variables with values form form."""
        request.content = self.content.data
        request.id_technician = self.technician.data

    def prefill(self, request):
        """Prefill form with request data."""
        self.content.data = request.content
        technicians = Technician.query.all()
        technicians_names = [(technician.id, technician.user.fullname) for technician in technicians]
        self.technician.choices = technicians_names


class TechnicianRequestForm(FlaskForm):
    content = TextAreaField('Description')
    estimated_time = DateField('Estimated Time', validators=[validate_estimated_time])
    real_time = FloatField('Real Time', validators=[NumberRange(min=0.5)])
    price = IntegerField('Price', validators=[NumberRange(min=1)])
    submit = SubmitField('Update request')

    def prefill(self, request):
        self.content.data = request.content
        self.estimated_time.data = request.estimated_time
        self.real_time.data = request.real_time
        self.price.data = request.price


class RequestCommentForm(FlaskForm):
    """From for adding request comment."""
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Add')

    def populate_comment(self, comment):
        """Populates comment variables with values submitted in form."""
        comment.content = self.content.data

    def submitted_and_valid(self):
        """Returns whether this form was submitted and is valid."""
        return self.submit.data and self.validate()

    def clear(self):
        """Clear form contents."""
        self.content.data = ""

class RequestEditCommentForm(FlaskForm):
    edit_id = IntegerField('Id', id="modal_edit_comment_id")
    edit_content = TextAreaField('Comment', id="modal_edit_comment_content", validators=[DataRequired()])
    edit_submit = SubmitField('Save')

    def populate_comment(self, comment):
        """Populates comment variables with values submitted in form."""
        comment.content = self.edit_content.data
        
    def submitted_and_valid(self):
        """Returns whether this form was submitted and is valid."""
        return self.edit_submit.data and self.validate()

class UpdateRequestForm(FlaskForm):
    """Form for updating service request as technician"""
    def __init__(self, submit_label=None, **kw):
        super(UpdateRequestForm, self).__init__(**kw)
        if submit_label is not None:
            self.submit.label.text = submit_label

    estimated_time = DateField('Expected completion date', validators=[validate_estimated_time])
    real_time = FloatField('Real time', validators=[validators.Optional(), NumberRange(min=0)])
    price = IntegerField('Price', validators=[validators.Optional(), NumberRange(min=0)])
    submit = SubmitField('Update Request')

    def populate_request(self, request):
        """Populates request variables with values form form."""
        request.estimated_time = self.estimated_time.data
        request.real_time = self.real_time.data
        request.price = self.price.data

    def prefill(self, request):
        """Prefill form with request data."""
        self.estimated_time.data = request.estimated_time
        self.real_time.data = request.real_time
        self.price.data = request.price
