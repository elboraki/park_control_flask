from models.database import db

class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    mot_passe = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relationships
    role = db.relationship('Role', backref='utilisateurs')
    
    def __repr__(self):
        return f'<Utilisateur {self.login}>' 