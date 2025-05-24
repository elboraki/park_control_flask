from flask import Blueprint, render_template, request, redirect, url_for
from services.user_service import UserService

users_bp = Blueprint('users_bp', __name__, url_prefix='/users')

@users_bp.route('/')
def list_users():
    users = UserService.list_users()
    return render_template('users/users.html', users=users)

@users_bp.route('/create', methods=['POST'])
def create_user():
    username = request.form['username']
    email = request.form['email']
    #UserService.create_user(username, email)
    return redirect(url_for('user_bp.list_users'))
