from models.database import db

class Etat(db.Model):
    __tablename__ = 'etats'
    
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f'<Etat {self.libelle}>' 