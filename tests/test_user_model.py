import pytest
from flask import Flask
from models.user import db, User

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session
def test_create_user(session):
    user = User(
        nom="Younes",
        prenom="El",
        login="younes123",
        password="secret",
        email="younes@example.com",
        role_id=1
    )
    session.add(user)
    session.commit()

    assert user.id is not None
    assert user.login == "younes123"
    assert user.email == "younes@example.com"
    

def test_user_repr():
    user = User(login="admin")
    assert repr(user) == "<User admin>"
