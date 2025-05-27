from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
from services.user_service import UserService
from models.user import User
users_bp = Blueprint('users_bp', __name__, url_prefix='/users')

@users_bp.route('/')
def list_users():
    page = request.args.get('page', 1, type=int)
    pagination = UserService.get_users_page(page, per_page=5)
    if request.args.get("query"):
        query=request.args.get("query")
        records=UserService.search_user_name(query)
        return render_template('users/users.html',users=records,pagination=pagination)
    else:
        return render_template('users/users.html', users=pagination.items, pagination=pagination)
    
    
    
@users_bp.route('/create', methods=['POST'])
def create_user():
    try:
        user = User(
            login=request.form['login'],
            prenom=request.form['prenom'],
            nom=request.form['nom'],
            email=request.form['email'],
            password=request.form['mot_passe'],
            role_id=request.form['role']
        )
        
        success = UserService.add_user(user)
        
        if success:
            flash("User added successfully!", "success")
        else:
            flash("User already exists or could not be added.", "warning")
        
    except Exception as e:
        flash(f"Error creating user: {str(e)}", "danger")
    
    return redirect(url_for('users_bp.list_users'))

@users_bp.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user=UserService.get_user_by_id(user_id)
        success = UserService.delete_user(user)
        if success==True:
            flash("User deleted successfully!", "success")
            return jsonify({'status': 'deleted'})
    except Exception as e:
        flash(f"Error deleting user: {str(e)}", "danger")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@users_bp.route('/edit/<int:user_id>', methods=['POST'])
def update_user(user_id):
    try:
        user = UserService.get_user_by_id(user_id)
        if not user:
            flash("User not found.", "warning")
            return redirect(url_for('users_bp.list_users'))

        # Update values from form
        user.login = request.form['login']
        user.prenom = request.form['prenom']
        user.nom = request.form['nom']
        user.email = request.form['email']
        user.password = request.form['mot_passe']
        user.role_id = request.form['role']

        success = UserService.update_user(user)

        if success:
            flash("Utiliateur a ete modifie!", "success")
            return jsonify({'status': 'updated'})
        else:
            flash("Erreur utilisiateur n'est pas modifie", "danger")
            return jsonify({'status': 'failed'})

    except Exception as e:
        flash(f"Error updating user: {str(e)}", "danger")

    return redirect(url_for('users_bp.list_users'))

