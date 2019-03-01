from flask import Blueprint, render_template
import config
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session,escape
from models.base_model import *
from models.user import *
from models.follow import *
from app import app 
from flask_login import current_user, login_required


follows_blueprint = Blueprint('follows',
                            __name__,
                            template_folder='templates')


@follows_blueprint.route('/<id>', methods=['POST'])
@login_required
def create_follow(id):
    user = User.get_by_id(id)
    already_followed = Follow.get_or_none(Follow.follower_user_id == current_user.id, Follow.followed_user_id==user.id)
    if request.method == "POST":
        if request.form.get('follow'):
            a = Follow(follower_user_id = current_user.id, followed_user_id= user.id)
            a.save()
            # if privacy_status = true, need approval before a user can follow
            # hence, update approved_status to False first, if approved, change to True
            if user.privacy_status:
                Follow.update(approved_status = False).where(Follow.follower_user_id == current_user.id, Follow.followed_user_id == user.id).execute()
        else:
            b = Follow.delete().where(Follow.follower_user_id == current_user.id, Follow.followed_user_id == user.id)
            b.execute()
    return redirect(url_for('users.show', username=user.username))

@follows_blueprint.route('/request', methods=["GET"])
def show_follow_requests():
    requests = Follow.select().where(Follow.approved_status == False , Follow.followed_user_id==current_user.id)
    return render_template('follows/request.html', requests=requests)

@follows_blueprint.route('/request/<id>', methods=["POST"])
def update_follow_requests(id):
    Follow.update(approved_status = True).where(Follow.followed_user_id==current_user.id, Follow.follower_user_id==id).execute()
    return redirect(url_for('follows.show_follow_requests'))

@follows_blueprint.route('/request/<id>/delete', methods=["POST"])
def destroy_follow_requests(id):
    Follow.delete().where(Follow.followed_user_id==current_user.id, Follow.follower_user_id==id).execute()
    return redirect(url_for('follows.show_follow_requests'))
    