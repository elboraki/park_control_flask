from flask import Flask,render_template
from config import Config
from models.database import db
from routes.users import users_bp
from routes.employees import employees_bp
from routes.vehicules import vehicules_bp
from routes.reservations import reservations_bp
from routes.dashboard import dashboard_bp
from routes.auth import auth_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@localhost/park_control'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24)  # For session management
    
    # Initialize the db with the app
    db.init_app(app)    

    with app.app_context(): 
        db.create_all()

    app.register_blueprint(users_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(vehicules_bp)
    app.register_blueprint(reservations_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
