from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, MultipleFileField, SelectField, BooleanField, \
    TimeField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed


class AddRequirementForm(FlaskForm):
    content = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Requirement')
    technician = SelectField(u'Technician')


class UpdateRequirementForm(FlaskForm):
    content = TextAreaField('Description')
    estimated_time = TimeField('Estimated Time')
    real_time = TimeField('Real Time')
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=1, message="Please enter a valid price.")])
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
