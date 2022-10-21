from time import strftime

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField, BooleanField,  DateField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed
from datetime import datetime


class AddRequirementForm(FlaskForm):
    content = TextAreaField('Description', validators=[DataRequired()])
    technician = SelectField(u'Technician', validators=[DataRequired()])
    submit = SubmitField('Create Requirement')


class UpdateRequirementForm(FlaskForm):
    content = TextAreaField('Description')
    estimated_time = DateField('Estimated Time')
    real_time = DateField('Real Time')
    price = IntegerField('Price')
    submit = SubmitField('Update requirement')

    def validate_on_submit(self):
        result = super(UpdateRequirementForm, self).validate()
        if self.estimated_time.data and self.estimated_time.data < datetime.date(datetime.today()):
            return False
        elif self.real_time.data and self.real_time.data < datetime.date(datetime.today()):
            return False
        elif self.price.data is None or self.price.data >= 0:
            return result
        else:
            return False

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
