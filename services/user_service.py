from repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def register_user(username, email, password):
        if UserRepository.get_by_email(email):
            raise Exception("Email already exists")
        return UserRepository.create(username, email, password)

    @staticmethod
    def list_users():
        return UserRepository.get_all()
    
    @staticmethod
    def get_users_page(page, per_page=5):
        return UserRepository.get_paginated(page, per_page)
    
    @staticmethod
    def search_user_name(query):
        return UserRepository.get_search_query(query)
    
    @staticmethod
    def add_user(data):
        return UserRepository.add(data)
    
    @staticmethod
    def delete_user(user):
        return UserRepository.delete(user)
    
    @staticmethod
    def update_user(user):
        return UserRepository.update(user)
    
    @staticmethod
    def get_user_by_id(user_id):
        return UserRepository.get_by_id(user_id)

