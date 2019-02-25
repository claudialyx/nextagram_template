from flask import Flask, render_template, request, redirect, Blueprint, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename
from app import app
from helpers import *
from models.base_model import BaseModel
from models.user import User
from models.image import Image
import datetime

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates/images')

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# to create new post/upload images 
def create_gallery_image(output):
    gallery_pic = Image(user_id=current_user.id, image_name = output)
    gallery_pic.save()

# to update profile image
def update_profile_pic(output):
    pic = User.update(profile_image_name = output).where(User.id == current_user.id)
    pic.execute()

# to send the file from the user’s computer directly to the bucket
@images_blueprint.route("/<id>", methods=["POST"])
def upload_file(id):
	# A
    if "user_file" not in request.files and "image_file" not in request.files:
        return "No file in request.files"

	# B If the key is in the object, we save it in a variable called file.
    if "user_file" in request.files:
        file = request.files["user_file"]
    if "image_file" in request.files:
        file = request.files["image_file"]
    """
        These attributes are also available
        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype
    """
	# C. We check the filename attribute on the object and if it’s empty, 
    # it means the user sumbmitted an empty form, so we return an error message.
    if file.filename == "":
        return "Please select a file"

	# D. we check that there is a file and that it has an allowed filetype
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, app.config['S3_BUCKET'])
        if "user_file" in request.files:
            update_profile_pic(output)
            return redirect(url_for("users.edit", id=id))
        if "image_file" in request.files:
            create_gallery_image(output)
            return redirect(url_for("users.show", username=current_user.username))
    else:
        return redirect("/<id>")

# user.profile_image_name # stored in database but returns just the path without domain

# function to upload a file to S3
def upload_file_to_s3(file, bucket_name, acl="public-read"):

    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    u_name = secure_filename(str(current_user.id) + file.filename + str(datetime.datetime.now()))

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            u_name,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    return u_name