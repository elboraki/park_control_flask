from flask import Blueprint, render_template, request, redirect, url_for
from services.user_service import UserService

users_bp = Blueprint('users_bp', __name__, url_prefix='/users')

@users_bp.route('/')
def list_users():
    page = request.args.get('page', 1, type=int)
    pagination = UserService.get_users_page(page, per_page=5)
    return render_template('users/users.html', users=pagination.items, pagination=pagination)
# @users_bp.route('/create', methods=['POST'])
# def create_user():
#     username = request.form['username']
#     email = request.form['email']
#     #UserService.create_user(username, email)
#     return redirect(url_for('user_bp.list_users'))
