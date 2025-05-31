from models.role import Role
from models.database import db

class RoleService:
    @staticmethod
    def get_all():
        return Role.query.all()
    
    @staticmethod
    def get_role_by_id(role_id):
        return Role.query.get(role_id)
    
    @staticmethod
    def create_role(libelle):
        role = Role(libelle=libelle)
        db.session.add(role)
        db.session.commit()
        return role
    
    @staticmethod
    def update_role(id, libelle):
        role = Role.query.get(id)
        if not role:
            raise Exception("Rôle non trouvé")
        
        role.libelle = libelle
        db.session.commit()
        return role
    
    @staticmethod
    def delete_role(id):
        role = Role.query.get(id)
        if not role:
            raise Exception("Rôle non trouvé")
        
        db.session.delete(role)
        db.session.commit()
        return True 