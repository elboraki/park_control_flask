from models.user import User, db

class UserRepository:
    @staticmethod
    def get_search_query(query):
        return User.query.filter(User.nom.ilike(f"%{query}%")).all()

    @staticmethod
    def get_paginated(page, per_page=5):
        return User.query.paginate(page=page, per_page=per_page)
    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def add(user):
        db.session.add(user)
        db.session.commit()

   

    @staticmethod
    def delete(user):
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Update failed: {e}")  # optional logging
            return False

    @staticmethod
    def update(user):
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Update failed: {e}")  # optional logging
            return False