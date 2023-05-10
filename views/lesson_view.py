from flask import Blueprint, request, jsonify
from server.controllers.lesson_controller import create_lesson

lesson_view = Blueprint('lesson_view', __name__)

@lesson_view.route('/lessons', methods=['POST'])
def add_lesson():
    title = request.json.get('title')
    description = request.json.get('description')

    if not title or not description:
        return jsonify({"error": "Title and description are required"}), 400

    lesson = create_lesson(title, description)
    return jsonify({"id": lesson.id, "title": lesson.title, "description": lesson.description}), 201
