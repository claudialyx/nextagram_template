from models.base_model import BaseModel
import peewee as pw
from models.user import User
from app import app

class Follow(BaseModel):
    follower_user_id = pw.ForeignKeyField(User, backref='follows')
    followed_user_id = pw.ForeignKeyField(User, backref='follows')
    approved_status = pw.BooleanField(default=True)
        
