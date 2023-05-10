# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

from server.views.lesson_view import lesson_view
from server.views.lesson_plan.lesson_plan_view import lesson_plan_view

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@localhost/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)

app.register_blueprint(lesson_view, url_prefix='/api')
app.register_blueprint(lesson_plan_view, url_prefix='/api/lesson_plan')

if __name__ == '__main__':
    app.run(debug=True)
