from flask import Flask,render_template
from config import Config
from models.database import db
from routes.users import users_bp
from routes.employees import employees_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize the db with the app
    db.init_app(app)    

    with app.app_context(): 
        db.create_all()

    app.register_blueprint(users_bp)
    app.register_blueprint(employees_bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
