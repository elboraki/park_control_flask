from models.database import db

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column("id",db.Integer, primary_key=True)
    name = db.Column("libelle",db.String(50))

    def __repr__(self):
        return f'<Role {self.name}>'

