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
@app.route("/")
def index():
#     # if 'user_id' in session:
#         # return redirect(url_for('index'))
    if current_user.is_authenticated:
        user_followings = Follow.select(Follow.followed_user_id).where(Follow.follower_user_id == current_user.id, Follow.approved_status == True)
        return render_template('users/home.html', user_followings=user_followings)
    else:
        return render_template('users/home.html')