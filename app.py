from flask_wtf.csrf import CSRFProtect
import os
import re
import config
from flask import Flask, render_template, request, redirect, url_for, flash, session,escape
from models.base_model import *
from flask_login import LoginManager, current_user,login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import braintree

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
csrf = CSRFProtect(app)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        # BT_ENVIRONMENT = os.environ.get("BT_ENVIRONMENT"),
        merchant_id= os.environ.get("BT_MERCHANT_ID"),
        public_key = os.environ.get("BT_PUBLIC_KEY"),
        private_key = os.environ.get("BT_PRIVATE_KEY")
    )
)

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

