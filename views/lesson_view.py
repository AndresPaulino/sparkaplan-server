from flask import Blueprint, request,jsonify
from controllers.lesson_controller import create_lesson
from models.lesson import Lesson

lesson_view = Blueprint('lesson_view', __name__)

@lesson_view.route('/generate-lesson', methods=['POST'])
def generate_lesson():
    grade = request.json.get('grade')
    lesson_title = request.json.get('lessonTitle')
    learning_objective = request.json.get('learningObjective')
    user_id = request.json.get('user_id')

    if not grade or not lesson_title or not learning_objective or not user_id:
        return jsonify({"error": "Grade, lesson title, and learning objective are required"}), 400

    lesson = create_lesson(grade, lesson_title, learning_objective, user_id)

    if lesson is None:
        return jsonify({"error": "Could not create lesson"}), 500

    return jsonify({
        "id": lesson.id, 
        "grade": lesson.grade, 
        "lesson_title": lesson.lesson_title,
        "learning_objective": lesson.learning_objective,
        "content": lesson.content
    }), 201

@lesson_view.route('/get-lesson', methods=['GET'])
def get_lesson():
    lesson_id = request.args.get('id')

    if not lesson_id:
        return jsonify({"error": "Lesson ID is required"}), 400

    lesson = Lesson.query.filter_by(id=lesson_id).first()

    if lesson is None:
        return jsonify({"error": "Could not find lesson"}), 404

    return jsonify({
        "id": lesson.id, 
        "grade": lesson.grade, 
        "lesson_title": lesson.lesson_title,
        "learning_objective": lesson.learning_objective,
        "content": lesson.content
    }), 200