from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from db import db
import os
from dotenv import load_dotenv
from views.lesson_view import lesson_view
from views.auth_view import auth_view
from views.user_view import user_view
from flask_jwt_extended import JWTManager
from datetime import timedelta

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_URI')}/{os.getenv('DB_NAME')}"
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)  # Set token expiration to 7 days
    jwt = JWTManager(app)
    
    db.init_app(app)
    migrate = Migrate(app, db)
    
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Register blueprint within the create_app function
    app.register_blueprint(lesson_view, url_prefix='/api')
    app.register_blueprint(auth_view, url_prefix='/api')
    app.register_blueprint(user_view, url_prefix='/api')
    
    
    return app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
