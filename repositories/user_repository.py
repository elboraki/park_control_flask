from models.user import User, db

class UserRepository:

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
    def create(username, email, password, user_type='normal'):
        user = User(username=username, email=email, password=password, user_type=user_type)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def delete(user):
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()
