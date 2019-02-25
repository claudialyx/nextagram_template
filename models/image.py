from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property
from app import app

class Image(BaseModel):
    user_id = pw.ForeignKeyField(User, backref='images')
    image_name = pw.CharField(index=True)
        
    @hybrid_property
    def show_gallery_image(self):
    # to display all users' images
        return app.config['S3_DOMAIN'] + str(self.image_name)