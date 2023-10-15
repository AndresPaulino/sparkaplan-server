from db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

class Lesson(db.Model):
    __tablename__ = 'lesson'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    grade = db.Column(db.String(30), nullable=False)
    lesson_title = db.Column(db.String(100), nullable=False)
    learning_objective = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)  # Ensure the table name matches User.__tablename__
