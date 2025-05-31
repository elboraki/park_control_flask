from models.database import db

class Role(db.Model):
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f'<Role {self.libelle}>'

