from flask import Blueprint, request, jsonify
from server.controllers.lesson_controller import create_lesson

lesson_view = Blueprint('lesson_view', __name__)

@lesson_view.route('/generate-lesson', methods=['POST'])
def generate_lesson():
    grade = request.json.get('grade')
    lesson_title = request.json.get('lessonTitle')
    learning_objective = request.json.get('learningObjective')

    if not grade or not lesson_title or not learning_objective:
        return jsonify({"error": "Grade, lesson title, and learning objective are required"}), 400

    lesson = create_lesson(grade, lesson_title, learning_objective)

    if lesson is None:
        return jsonify({"error": "Could not create lesson"}), 500

    return jsonify({
        "id": lesson.id, 
        "grade": lesson.grade, 
        "lesson_title": lesson.lesson_title,
        "learning_objective": lesson.learning_objective,
        "content": lesson.content
    }), 201
