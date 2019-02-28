from flask import Blueprint, render_template
from flask_wtf.csrf import CSRFProtect
import os
import re
import config
from flask import Flask, render_template, request, redirect, url_for, flash, session,escape
from models.base_model import *
from models.user import *
from flask_login import LoginManager, current_user,login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app 
from peewee import fn
from authlib.flask.client import OAuth

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates/users')

@users_blueprint.route('/new', methods=['GET'])
def new():
    if current_user.is_authenticated:
        return redirect('/')
    return render_template('signup.html')


@users_blueprint.route('/', methods=['POST'])
def create():
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
        login_user(new_user)
        return redirect(url_for('index'))
    else:
        return render_template('signup.html', errors=new_user.errors)
    
    return render_template('signup.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get(User.username == username)
    post_count = len(user.images)
    return render_template('profile_page.html', user=user, post_count=post_count)

@users_blueprint.route('/search', methods=["POST"])
def search():
    search_user = request.form.get('search_user')
    user = User.get(User.username == search_user)
    return redirect(url_for('users.show', username=user.username))

@users_blueprint.route('/', methods=["GET"])
def index():
    return render_template('home.html')

@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    return render_template('edit_profile.html')

@users_blueprint.route('/<id>/edit/account_privacy', methods=['GET'])
@login_required
def edit_account_privacy(id): 
    return render_template('account_privacy.html')

@users_blueprint.route('/<id>/update/account_privacy', methods=['POST'])
@login_required
def update_account_privacy(id): 
    if request.form.get('account_privacy'):
        user= User.get(id=id)
        new_privacy = not user.privacy_status
        a = User.update(privacy_status = new_privacy ).where(User.id == current_user.id).execute()
        flash("Account privacy status updated")
    return redirect(url_for('users.edit_account_privacy',id=current_user.id))

@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user = User.get_by_id(current_user.id)

    if request.method =="POST":
        user_username = request.form.get('username_edit')
        user_email = request.form.get('email_edit')
        user_old_password = request.form.get('old_password')
        user_new_password = request.form.get('new_password')
        user_confirm_new_password = request.form.get('confirm_password')

        if current_user == user:
            if user_username:
                q = User.update(username=user_username).where(User.id == user)
            if user_email:
                q = User.update(email=user_email).where(User.id == user)
            if user_new_password:
                if re.match(r'[A-Za-z0-9@#$%^&+=]{6,}', user_new_password):
                    if check_password_hash(current_user.password,user_old_password) and user_new_password == user_confirm_new_password:
                        hashed_password = generate_password_hash(user_new_password) 
                        q = User.update(password=hashed_password).where(User.id == user)
                    else: 
                        flash("Please ensure that your old password is correct and reconfirm your new passwords")
                        return render_template('edit_profile.html')
                else:   
                    flash ("Password must be at least 6 characters long")
                    return render_template('edit_profile.html')

            q.execute()
            flash("Successfully updated")
            return redirect(url_for('users.edit', id=current_user.id))
        else:
            return render_template('edit_profile.html')
    return render_template('edit_profile.html')