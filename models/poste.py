from models.database import db

class Poste(db.Model):
    __tablename__ = 'postes'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column("titre",db.String(100), nullable=False)
    
    employees = db.relationship('Employee', backref='poste', lazy=True)
    
    def __repr__(self):
        return f'<Poste {self.titre}>'

