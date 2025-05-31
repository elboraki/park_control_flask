# models/user.py
from models.database import db

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    date_hire = db.Column("date_embauche",db.Date, nullable=False)
    poste_id = db.Column(db.Integer, db.ForeignKey('postes.id'), nullable=False)
    
    def __repr__(self):
        return f'<Employee {self.nom} {self.prenom}>'
