# models/user.py
from models.database import db
from models.role import Role

class User(db.Model):
    __tablename__ = 'utilisateurs'

    id = db.Column("id",db.Integer, primary_key=True)
    nom = db.Column("nom",db.String(50))
    prenom = db.Column("prenom",db.String(50))
    login = db.Column("login",db.String(50))
    password = db.Column("mot_passe",db.String(50))
    email = db.Column("email",db.String(50),unique=True)
    role_id = db.Column("role_id", db.Integer, db.ForeignKey('roles.id'))  
    
    role = db.relationship('Role', backref='users')
    
    def __repr__(self):
        return f'<User {self.login}>'
