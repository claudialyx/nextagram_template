from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from instagram_web.blueprints.follows.views import follows_blueprint
from flask_login import current_user
from flask_assets import Environment, Bundle
from .util.assets import bundles
import config
from instagram_web.helpers.google_oauth import *

oauth.init_app(app)

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(follows_blueprint, url_prefix="/follows")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

from models.follow import Follow
from models.image import Image
# from models.user import User
@app.route("/")
def index():
#     # if 'user_id' in session:
#         # return redirect(url_for('index'))
    if current_user.is_authenticated:
        user_followings = Follow.select().where(Follow.follower_user_id == current_user.id, Follow.approved_status == True)
        followings_id = list(follow.followed_user_id for follow in user_followings)
        user_followings_images = Image.select().where(Image.user_id << followings_id).order_by(Image.created_at.desc())
        # breakpoint()
        return render_template('users/home.html', user_followings_images=user_followings_images)
    else:
        return render_template('users/home.html')