from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from db import db
import os
from dotenv import load_dotenv
from views.lesson_view import lesson_view

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}"
    
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Register blueprint within the create_app function
    app.register_blueprint(lesson_view, url_prefix='/api')
    
    return app

app = create_app()
CORS(app, supports_credentials=True)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
