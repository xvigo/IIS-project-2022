from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, NumberRange, Optional
from flask_wtf.file import FileAllowed
from TownIssues.tickets.utils import save_image
from TownIssues.models import Image

class AddTicketForm(FlaskForm):
    """Form for adding new ticket."""
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    house_num = IntegerField('House Number', validators=[Optional(), NumberRange(min=1, message="Please enter a valid house number.")])
    picture = MultipleFileField('Choose pictures', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Create Ticket')

    def populate_ticket(self, ticket):
        """Populates given ticket variables with values submitted in form."""
        ticket.title = self.title.data
        ticket.content = self.content.data
        ticket.street = self.street.data
        ticket.house_number = self.house_num.data 

        for form_image in self.picture.data:
            if form_image.filename:
                picture = save_image(form_image)
                image = Image(url='/static/ticket_pics/' + picture)
                ticket.images.append(image)

class UpdateTicketForm(FlaskForm):
    """Form for updating existing ticket."""
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    house_num = IntegerField('House Number', validators=[Optional(), NumberRange(min=1, message="Please enter a valid house number.")])
    picture = MultipleFileField('Add new pictures', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Ticket')

    def prefill(self, ticket):
        """Prefills form with values form given form."""
        self.title.data = ticket.title
        self.content.data = ticket.content
        self.street.data = ticket.street
        self.house_num.data = ticket.house_number

    def populate_ticket(self, ticket):
        """Populates given ticket variables with values submitted in form."""
        ticket.title = self.title.data
        ticket.content = self.content.data
        ticket.street = self.street.data
        ticket.house_number = self.house_num.data 

        for form_image in self.picture.data:
            if form_image.filename:
                picture = save_image(form_image)
                image = Image(url='/static/ticket_pics/' + picture)
                ticket.images.append(image)


class AddCommentForm(FlaskForm):
    """Form for adding new ticket comment."""
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Add Comment')

    def populate_comment(self, comment):
        """Populates given comment variables with values submitted in form."""
        comment.content = self.content.data

    def submitted_and_valid(self):
        """Returns whether this form was submitted and is valid."""
        return self.submit.data and self.validate()

    def clear(self):
        """Clear form contents."""
        self.content.data = ""

class EditCommentForm(FlaskForm):
    """Form for updating existing ticket comment."""
    edit_id = IntegerField('Id', id="modal_edit_comment_id")
    edit_content = TextAreaField('Comment', id="modal_edit_comment_content", validators=[DataRequired()])
    edit_submit = SubmitField('Save')

    def prefill(self, comment):
        """Prefills form with values form given comment."""
        self.edit_id.data = comment.id
        self.edit_content.data = comment.content

    def populate_comment(self, comment):
        """Populates given comment variables with values submitted in form."""
        comment.content = self.edit_content.data

    def submitted_and_valid(self):
        """Returns whether this form was submitted and is valid."""
        return self.edit_submit.data and self.validate()