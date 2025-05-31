from models.database import db
from datetime import datetime

class Reservation(db.Model):
    __tablename__ = 'reservations'
    
    id = db.Column(db.Integer, primary_key=True)
    date_reservation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_debut = db.Column(db.DateTime, nullable=False)
    date_fin = db.Column(db.DateTime, nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    vehicule_id = db.Column(db.Integer, db.ForeignKey('vehicules.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    
    # Relationships
    utilisateur = db.relationship('Utilisateur', backref='reservations')
    vehicule = db.relationship('Vehicule', backref='reservations')
    employee = db.relationship('Employee', backref='reservations')
    
    def __repr__(self):
        return f'<Reservation {self.id}>' 