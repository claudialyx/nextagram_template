from models.base_model import BaseModel
from flask_login import UserMixin
import peewee as pw
from playhouse.hybrid import hybrid_property
from app import app


class User(BaseModel, UserMixin):
    # id = pw.IntegerField(primary_key=True)
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(index=True)
    profile_image_path = pw.CharField(null=True) 

    def validate(self):
        duplicate_users = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_users:
            self.errors.append('Username not unique. Please choose another username.')
        if duplicate_email:
            self.errors.append('This email address has been used.')

    @hybrid_property
    def profile_image_url(self):
        return app.config['S3_DOMAIN'] + self.profile_image_path    