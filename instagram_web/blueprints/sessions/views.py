from flask import Blueprint, render_template
from models.base_model import *
from models.user import *
from flask import Flask, render_template, request, redirect, url_for, flash, session,escape
from flask_login import LoginManager, current_user,login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates/sessions')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))
    
@sessions_blueprint.route("/user")
def index_user():
    return render_template('signin.html')

@sessions_blueprint.route("/user/sign_in", methods=['GET','POST'])
def sign_in():
    if current_user.is_authenticated:
        return render_template('home.html')
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
                # flash("The current user is" + current_user.username)
                return redirect(url_for('index'))
            else: 
                flash("Please ensure username and password are correct")
                return render_template('signin.html')
        else: 
            flash("Please ensure username and password are correct")
            return render_template('signin.html')
    return render_template('signin.html')

@sessions_blueprint.route("/user/sign_out")
@login_required
def sign_out():
    logout_user()
    # remove the username from the session if it's there
    # session.pop('user_id', None)
    flash("Successfully signed out")
    return redirect(url_for('index'))

