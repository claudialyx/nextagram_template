from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
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

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# from models.user import User
from models.follow import Follow
#before
# @app.route("/")
# def index():
# #     # if 'user_id' in session:
# #         # return redirect(url_for('index'))
#     users = User.select()
#     return render_template('users/home.html', users=users)

@app.route("/")
def index():
#     # if 'user_id' in session:
#         # return redirect(url_for('index'))
    # user_followings = User.get(Follow.follower_user_id==current_user.id)
    # user_followings = User.select().join(Follow, on=(Follow.follower_user_id == current_user.id))
    user_followings = Follow.select(Follow.followed_user_id).where(Follow.follower_user_id == current_user.id)

    return render_template('users/home.html', user_followings=user_followings)


# to obtain all users we are following:
# User.follows.followed_user_id

# to obtain all images of a particular user:
# User.images.image_name
