from flask import Flask,render_template
from config import Config
from models.user import db
from routes.users import users_bp
def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)    
    app.register_blueprint(users_bp)

    with app.app_context(): 
        db.create_all()

    return app


if __name__ == '__main__':
    app=create_app()
    app.run(debug=True)
