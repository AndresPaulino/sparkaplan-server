from server import db

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(30), nullable=False)
    lesson_title = db.Column(db.String(100), nullable=False)
    learning_objective = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)  # Storing the OpenAI generated content
