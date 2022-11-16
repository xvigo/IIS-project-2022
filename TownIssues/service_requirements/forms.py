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

class AddRequirementForm(FlaskForm):
    """Form for adding service requirement."""

    def __init__(self, submit_label = None, **kw):
        super(AddRequirementForm, self).__init__(**kw)
        if submit_label is not None:
            self.submit.label.text = submit_label

    content = TextAreaField('Description', validators=[DataRequired()])
    technician = SelectField('Technician', validators=[DataRequired()])
    submit = SubmitField('Create Requirement')

    def init_technicians(self):
        """Add technicians to form select field."""
        technicians = Technician.query.all()
        technicians_names = [(technician.id, technician.user.fullname) for technician in technicians]
        self.technician.choices = technicians_names

    def populate_requirement(self, requirement):
        """Populates requirement variables with values form form."""
        requirement.content = self.content.data
        requirement.id_technician = self.technician.data

    def prefill(self, requirement):
        """Prefill form with requirement data."""
        self.content.data = requirement.content
        technicians = Technician.query.all()
        technicians_names = [(technician.id, technician.user.fullname) for technician in technicians]
        self.technician.choices = technicians_names


class TechnicianRequirementForm(FlaskForm):
    content = TextAreaField('Description')
    estimated_time = DateField('Estimated Time', validators=[validate_estimated_time])
    real_time = FloatField('Real Time', validators=[NumberRange(min=0)])
    price = IntegerField('Price', validators=[NumberRange(min=0)])
    submit = SubmitField('Update requirement')

    def prefill(self, requirement):
        self.content.data = requirement.content
        self.estimated_time.data = requirement.estimated_time
        self.real_time.data = requirement.real_time
        self.price.data = requirement.price


class RequirementCommentForm(FlaskForm):
    """From for adding requirement comment."""
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

class RequirementEditCommentForm(FlaskForm):
    edit_id = IntegerField('Id', id="modal_edit_comment_id")
    edit_content = TextAreaField('Comment', id="modal_edit_comment_content", validators=[DataRequired()])
    edit_submit = SubmitField('Save')

    def populate_comment(self, comment):
        """Populates comment variables with values submitted in form."""
        comment.content = self.edit_content.data
        
    def submitted_and_valid(self):
        """Returns whether this form was submitted and is valid."""
        return self.edit_submit.data and self.validate()

class UpdateRequirementForm(FlaskForm):
    """Form for updating service requirement as technician"""
    def __init__(self, submit_label=None, **kw):
        super(UpdateRequirementForm, self).__init__(**kw)
        if submit_label is not None:
            self.submit.label.text = submit_label

    estimated_time = DateField('Estimated time', validators=[validate_estimated_time])
    real_time = FloatField('Real time', validators=[validators.Optional(), NumberRange(min=0)])
    price = IntegerField('Price', validators=[validators.Optional(), NumberRange(min=0)])
    submit = SubmitField('Update Requirement')

    def populate_requirement(self, requirement):
        """Populates requirement variables with values form form."""
        requirement.estimated_time = self.estimated_time.data
        requirement.real_time = self.real_time.data
        requirement.price = self.price.data

    def prefill(self, requirement):
        """Prefill form with requirement data."""
        self.estimated_time.data = requirement.estimated_time
        self.real_time.data = requirement.real_time
        self.price.data = requirement.price
