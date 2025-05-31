from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.utilisateur import Utilisateur
from models.database import db
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Veuillez vous connecter pour accéder à cette page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = Utilisateur.query.filter_by(email=email).first()
        
        if user and user.mot_passe == password:  # In production, use proper password hashing!
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_nom'] = user.nom
            session['user_prenom'] = user.prenom
            session['user_role'] = user.role_id
            flash('Connexion réussie!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Email ou mot de passe incorrect.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('auth.login')) 