from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for, session
from services.user_service import UserService
from models.utilisateur import Utilisateur
from models.database import db
from routes.auth import login_required
from functools import wraps
from forms.user_form import UserForm
from services.role_service import RoleService

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
    form = UserForm()
    form.role_id.choices = [(r.id, r.libelle) for r in RoleService.get_all()]
    
    if request.args.get("query"):
        query = request.args.get("query")
        records = UserService.search_users(query)
        return render_template('users/users.html', 
                             users=records,
                             pagination=pagination,
                             form=form)
    else:
        return render_template('users/users.html', 
                             users=pagination.items, 
                             pagination=pagination,
                             form=form)

@users_bp.route('/search')
def search_users():
    query = request.args.get('query', '')
    users = UserService.search_users(query)
    return jsonify([{
        'id': user.id,
        'nom': user.nom,
        'prenom': user.prenom,
        'email': user.email,
        'login': user.login,
        'role': user.role.libelle if user.role else ''
    } for user in users])

@users_bp.route('/add', methods=['POST'])
@login_required
@admin_required
def add_user():
    form = UserForm()
    form.role_id.choices = [(r.id, r.libelle) for r in RoleService.get_all()]
    
    if form.validate_on_submit():
        UserService.create_user(
            nom=form.nom.data,
            prenom=form.prenom.data,
            email=form.email.data,
            login=form.login.data,
            mot_passe=form.mot_passe.data,
            role_id=form.role_id.data
        )
        flash('Utilisateur ajouté avec succès!', 'success')
        return redirect(url_for('users_bp.list_users'))
    
    flash('Erreur lors de l\'ajout de l\'utilisateur.', 'error')
    return redirect(url_for('users_bp.list_users'))

@users_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    if request.method == 'GET':
        user = UserService.get_user_by_id(id)
        return jsonify({
            'id': user.id,
            'nom': user.nom,
            'prenom': user.prenom,
            'email': user.email,
            'login': user.login,
            'role_id': user.role_id
        })
    
    # Handle POST request
    data = request.get_json()
    try:
        UserService.update_user(
            id=id,
            nom=data.get('nom'),
            prenom=data.get('prenom'),
            email=data.get('email'),
            login=data.get('login'),
            role_id=data.get('role_id'),
            mot_passe=data.get('mot_passe')
        )
        return jsonify({'success': True, 'message': 'Utilisateur modifié avec succès!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@users_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    try:
        UserService.delete_user(id)
        flash('Utilisateur supprimé avec succès!', 'success')
        return jsonify({'success': True})
    except Exception as e:
        flash('Erreur lors de la suppression de l\'utilisateur.', 'error')
        return jsonify({'success': False, 'error': str(e)}), 400

