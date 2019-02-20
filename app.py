from flask_wtf.csrf import CSRFProtect
import os
import re
import config
from flask import Flask, render_template, request, redirect, url_for
from models.base_model import *
from models.user import *
from werkzeug.security import generate_password_hash

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
csrf = CSRFProtect(app)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response

@app.route("/")
def homepage():
    return render_template('home.html')

@app.route("/users/sign_in")
def sign_in():
    return render_template('signin.html')

@app.route("/users/new")
def new_user():
    return render_template('signup.html')

@app.route("/users/", methods=["POST"])
def create_user():
    message = []
    user_username = request.form['username_up']
    user_email = request.form['email_up']
    user_password = request.form['password_up']

    if re.match(r'[A-Za-z0-9@#$%^&+=]{6,}', user_password):
        hashed_password = generate_password_hash(user_password) 
    else:
        pw_message = "Password must be at least 6 characters long"
        return render_template('signup.html', pw_message=pw_message)
         
    new_user = User(username=user_username,email=user_email,password=hashed_password)
    
    if new_user.save():
        message.append("Successfully signed up! You may proceed to sign in now.")
        return redirect(url_for('new_user', message=message))
    else:
        return render_template('signup.html', errors=new_user.errors)
    
    return render_template('signup.html')