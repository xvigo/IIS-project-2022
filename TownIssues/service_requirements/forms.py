from time import strftime

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField, BooleanField, DateField, \
    TimeField, FloatField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from flask_wtf.file import FileField, FileAllowed
from datetime import datetime


def validate_estimated_time(form, field):
    if field.data and field.data < datetime.date(datetime.today()):
        raise ValidationError('Estimated time cannot be in past')

class AddRequirementForm(FlaskForm):
    content = TextAreaField('Description', validators=[DataRequired()])
    technician = SelectField(u'Technician', validators=[DataRequired()])
    submit = SubmitField('Create Requirement')


class UpdateRequirementForm(FlaskForm):
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
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Add')


class RequirementEditCommentForm(FlaskForm):
    edit_id = IntegerField('Id', id="modal_edit_comment_id")
    edit_content = TextAreaField('Comment', id="modal_edit_comment_content", validators=[DataRequired()])
    edit_submit = SubmitField('Save')
