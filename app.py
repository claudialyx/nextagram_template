from flask_wtf.csrf import CSRFProtect
import os
import re
import config
from flask import Flask, render_template, request, redirect, url_for, flash, session,escape
from models.base_model import *
from models.user import *
from flask_login import LoginManager, current_user,login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

# how to use css styles using {%% } ??? 

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)

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

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 404 status explicitly
    return render_template('500.html'), 500

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route("/")
def index():
    # if 'user_id' in session:
        # return redirect(url_for('index'))
    return render_template('home.html')

@app.route("/user")
def index_user():
    return render_template('signin.html')

@app.route("/user/sign_in", methods=['GET','POST'])
def sign_in():
    if request.method == "POST":
        username_to_check = request.form['username_in']
        password_to_check = request.form['password_in']

        user = User.get_or_none(User.username == username_to_check)
        if user:
            hashed_password = user.password
            result = check_password_hash(hashed_password, password_to_check)
            if result:
                # session["user_id"] = user.id # tells the browser to store `user.id` in session with the key as `user_id`
                login_user(user)
                flash("The current user is" + current_user.username)
                return redirect(url_for('index'))
            else: 
                flash("Please ensure username and password are correct")
                return render_template('signin.html')
        else: 
            flash("Please ensure username and password are correct")
            return render_template('signin.html')
    return render_template('signin.html')

@app.route("/user/sign_out")
@login_required
def sign_out():
    logout_user()
    # remove the username from the session if it's there
    # session.pop('user_id', None)
    flash("Successfully signed out")
    return redirect(url_for('index'))

@app.route("/users/new")
def new_user():
    return render_template('signup.html')

@app.route("/users/", methods=["POST"])
def create_user():
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
        flash("Successfully signed up!")
        return redirect(url_for('index'))
    else:
        breakpoint()
        return render_template('signup.html', errors=new_user.errors)
    
    return render_template('signup.html')