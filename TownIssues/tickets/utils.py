from flask import current_app
import os
import secrets

def save_image(form_image):
    """Saves image from form to filesystem."""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/ticket_pics/' + picture_fn)
    form_image.save(picture_path)
    
    return picture_fn


def delete_images_from_tickets(tickets):
    """Deletes images of given tickets from file system."""   
    for ticket in tickets:
        for image in ticket.images:
            path = 'TownIssues' + image.url
            if os.path.exists(path):
                os.remove(path)


def delete_orphan_images():
    """Development route for deleting orphan image files."""
    from TownIssues.models import Image
    from TownIssues import db

    files_to_delete = os.listdir('TownIssues/static/ticket_pics')
    images = Image.query.all()
    for image in images:
        try:
            filename = os.path.basename(image.url)
            files_to_delete.remove(filename)
        except ValueError:
            db.session.delete(image)

    db.session.commit()
    for file in files_to_delete:
        file_path = 'TownIssues/static/ticket_pics/' + file
        if os.path.exists(file_path):
            os.remove(file_path)