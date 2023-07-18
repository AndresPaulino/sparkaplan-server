import uuid
from datetime import datetime
from db import db

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=str(uuid.uuid4()))
    grade = db.Column(db.String(30), nullable=False)
    lesson_title = db.Column(db.String(100), nullable=False)
    learning_objective = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)  # Storing the OpenAI generated content
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # It establishes a foreign key relationship with User model
