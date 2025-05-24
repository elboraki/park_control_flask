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
