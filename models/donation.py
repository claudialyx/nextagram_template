from models.base_model import BaseModel
import peewee as pw
from models.user import User
from models.image import Image
from playhouse.hybrid import hybrid_property
from app import app

class Donation(BaseModel):
    amount = pw.DecimalField(null=False, decimal_places=2)
    image_id = pw.ForeignKeyField(Image, backref='donations')
    donor_user_id = pw.ForeignKeyField(User, backref='donations')
