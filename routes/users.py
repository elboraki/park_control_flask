from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for, session
from services.user_service import UserService
from models.user import User
from models.utilisateur import Utilisateur
from models.database import db
from routes.auth import login_required
from functools import wraps

users_bp = Blueprint('users_bp', __name__, url_prefix='/users')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_role') == 1:  # Assuming role_id 1 is admin
            flash('Accès non autorisé. Droits administrateur requis.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@users_bp.route('/')
@login_required
@admin_required
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
@login_required
@admin_required
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
@login_required
@admin_required
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
@login_required
@admin_required
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

@users_bp.route('/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    if request.method == 'POST':
        email = request.form.get('email')
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        mot_passe = request.form.get('mot_passe')
        role_id = request.form.get('role_id')
        login = request.form.get('login')

        # Check if email already exists
        if Utilisateur.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé.', 'danger')
            return redirect(url_for('users_bp.add'))

        # Check if login already exists
        if Utilisateur.query.filter_by(login=login).first():
            flash('Ce login est déjà utilisé.', 'danger')
            return redirect(url_for('users_bp.add'))

        new_user = Utilisateur(
            email=email,
            nom=nom,
            prenom=prenom,
            mot_passe=mot_passe,
            role_id=role_id,
            login=login
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Utilisateur ajouté avec succès!', 'success')
            return redirect(url_for('users_bp.list_users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de l\'ajout de l\'utilisateur: {str(e)}', 'danger')

    return render_template('users/add_user.html')

@users_bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    user = Utilisateur.query.get_or_404(id)
    
    if request.method == 'POST':
        email = request.form.get('email')
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        role_id = request.form.get('role_id')
        login = request.form.get('login')
        
        # Check if email is changed and already exists
        if email != user.email and Utilisateur.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé.', 'danger')
            return redirect(url_for('users_bp.edit', id=id))
            
        # Check if login is changed and already exists
        if login != user.login and Utilisateur.query.filter_by(login=login).first():
            flash('Ce login est déjà utilisé.', 'danger')
            return redirect(url_for('users_bp.edit', id=id))

        try:
            user.email = email
            user.nom = nom
            user.prenom = prenom
            user.role_id = role_id
            user.login = login
            
            # Only update password if a new one is provided
            new_password = request.form.get('mot_passe')
            if new_password:
                user.mot_passe = new_password

            db.session.commit()
            flash('Utilisateur modifié avec succès!', 'success')
            return redirect(url_for('users_bp.list_users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la modification de l\'utilisateur: {str(e)}', 'danger')

    return render_template('users/edit_user.html', user=user)

@users_bp.route('/users/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete(id):
    user = Utilisateur.query.get_or_404(id)
    
    # Prevent self-deletion
    if user.id == session.get('user_id'):
        flash('Vous ne pouvez pas supprimer votre propre compte.', 'danger')
        return redirect(url_for('users_bp.list_users'))
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash('Utilisateur supprimé avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression de l\'utilisateur: {str(e)}', 'danger')
    
    return redirect(url_for('users_bp.list_users'))

