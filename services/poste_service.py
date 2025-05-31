from models.poste import Poste
from models.database import db

class PosteService:
    @staticmethod
    def get_all():
        return Poste.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Poste.query.get(id)
    
    @staticmethod
    def create_poste(libelle):
        poste = Poste(libelle=libelle)
        db.session.add(poste)
        db.session.commit()
        return poste 