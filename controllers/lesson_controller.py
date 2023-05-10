# controllers/lesson_controller.py
from server.models.lesson import Lesson
from server import db

def create_lesson(title, description):
    lesson = Lesson(title=title, description=description)
    db.session.add(lesson)
    db.session.commit()
    return lesson
