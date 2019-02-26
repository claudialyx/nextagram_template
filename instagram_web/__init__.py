from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donations_blueprint, url_prefix="/donations")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

from models.user import User
@app.route("/")
def index():
#     # if 'user_id' in session:
#         # return redirect(url_for('index'))
    users = User.select()
    return render_template('home.html', users=users)
    # return render_template('home.html')

