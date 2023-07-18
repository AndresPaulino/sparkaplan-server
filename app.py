from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@localhost/dbname"
db = SQLAlchemy(app)

from server.views.lesson_view import lesson_view

# Register blueprint
app.register_blueprint(lesson_view, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)
