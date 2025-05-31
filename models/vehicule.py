from models.database import db

class Vehicule(db.Model):
    __tablename__ = 'vehicules'
    
    id = db.Column(db.Integer, primary_key=True)
    immatriculation = db.Column(db.String(20), unique=True, nullable=False)
    marque = db.Column(db.String(50), nullable=False)
    modele = db.Column(db.String(50), nullable=False)
    etat_id = db.Column(db.Integer, db.ForeignKey('etats.id'), nullable=False)
    
    # Relationships
    etat = db.relationship('Etat', backref='vehicules')
    
    def __repr__(self):
        return f'<Vehicule {self.immatriculation}>' 