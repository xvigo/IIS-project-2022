from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, MultipleFileField, SelectField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed


class AddRequirementForm(FlaskForm):
    content = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Requirement')
    technician = SelectField(u'Technician')


class UpdateRequirementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    house_num = IntegerField('House Number', validators=[DataRequired(), NumberRange(min=1,
                                                                                     message="Please enter a valid house number.")])
    picture = MultipleFileField('Choose picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Ticket')

    def prefill(self, ticket):
        self.title.data = ticket.title
        self.content.data = ticket.content
        self.street.data = ticket.street
        self.house_num.data = ticket.house_number


class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Add')


class EditCommentForm(FlaskForm):
    edit_id = IntegerField('Id', id="modal_edit_comment_id")
    edit_content = TextAreaField('Comment', id="modal_edit_comment_content", validators=[DataRequired()])
    edit_submit = SubmitField('Save')
