from models.utilisateur import Utilisateur
from models.database import db
from sqlalchemy import or_

class UserService:
    @staticmethod
    def register_user(username, email, password):
        if UserRepository.get_by_email(email):
            raise Exception("Email already exists")
        return UserRepository.create(username, email, password)

    @staticmethod
    def list_users():
        return UserRepository.get_all()
    
    @staticmethod
    def get_users_page(page, per_page=5):
        return Utilisateur.query.order_by(Utilisateur.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def search_users(query):
        return Utilisateur.query.filter(
            or_(
                Utilisateur.nom.ilike(f'%{query}%'),
                Utilisateur.prenom.ilike(f'%{query}%'),
                Utilisateur.email.ilike(f'%{query}%'),
                Utilisateur.login.ilike(f'%{query}%')
            )
        ).all()
    
    @staticmethod
    def add_user(data):
        return UserRepository.add(data)
    
    @staticmethod
    def delete_user(id):
        user = Utilisateur.query.get(id)
        if not user:
            raise Exception("Utilisateur non trouvé")
        
        db.session.delete(user)
        db.session.commit()
        return True
    
    @staticmethod
    def update_user(id, nom, prenom, email, login, role_id, mot_passe=None):
        user = Utilisateur.query.get(id)
        if not user:
            raise Exception("Utilisateur non trouvé")

        user.nom = nom
        user.prenom = prenom
        user.email = email
        user.login = login
        user.role_id = role_id
        if mot_passe:
            user.mot_passe = mot_passe

        db.session.commit()
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        return Utilisateur.query.get(user_id)

    @staticmethod
    def create_user(nom, prenom, email, login, mot_passe, role_id):
        user = Utilisateur(
            nom=nom,
            prenom=prenom,
            email=email,
            login=login,
            mot_passe=mot_passe,
            role_id=role_id
        )
        db.session.add(user)
        db.session.commit()
        return user

