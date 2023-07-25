from flask import Blueprint, request,jsonify
from flask_cors import cross_origin
from controllers.lesson_controller import LessonController, create_lesson

lesson_view = Blueprint('lesson_view', __name__)

#######################################
# -------- [ Lesson Routes ] -------- #
#######################################


# ======== [ Generate Lesson ] ======== #
@lesson_view.route('/generate-lesson', methods=['POST'])
@cross_origin()
def generate_lesson():
    grade = request.json.get('grade')
    lesson_title = request.json.get('lessonTitle')
    learning_objective = request.json.get('learningObjective')
    user_id = request.json.get('user_id')

    if not grade or not lesson_title or not learning_objective or not user_id:
        return jsonify({"error": "Grade, lesson title, learning objective, and user ID are required"}), 400

    lesson = create_lesson(grade, lesson_title, learning_objective, user_id)

    if lesson is None:
        return jsonify({"error": "Could not create lesson"}), 500

    return jsonify({
        "id": lesson.id, 
        "grade": lesson.grade, 
        "lesson_title": lesson.lesson_title,
        "learning_objective": lesson.learning_objective,
        "content": lesson.content,
        "date_created": lesson.date_created,
    }), 201

# ======== [ Get Lesson ] ======== #
@lesson_view.route('/get-lesson/<id>', methods=['GET'])
@cross_origin()
def get_lesson(id):
    if not id:
        return jsonify({"error": "Lesson ID is required"}), 400

    try:
        lesson = LessonController.get_by_id(id)
        if lesson is None:
            return jsonify({"error": "Could not find lesson"}), 404

        return jsonify(lesson), 200
    except Exception as e:
        print(f"Error getting lesson: {e}")
        return jsonify({"error": "Could not get lesson"}), 500
    

# ======== [ Get All Lessons ] ======== #
@lesson_view.route('/get-all-lessons', methods=['GET'])
def get_all_lessons():
    lessons = LessonController.get_all()
    if lessons is None:
        return jsonify(message='Error getting lessons'), 500
    return jsonify(lessons=lessons), 200

# ======== [ Delete Lesson ] ======== #
@lesson_view.route('/delete-lesson/<id>', methods=['DELETE'])
def delete_lesson(id):
    if not id:
        return jsonify({"error": "Lesson ID is required"}), 400

    try:
        lesson = LessonController.get_by_id(id)
        if lesson is None:
            return jsonify({"error": "Could not find lesson"}), 404

        LessonController.delete(lesson)
        return jsonify(message='Lesson deleted'), 200
    except Exception as e:
        print(f"Error deleting lesson: {e}")
        return jsonify({"error": "Could not delete lesson"}), 500

# ======== [ Delete Multiple Lessons ] ======== #
@lesson_view.route('/delete-lessons', methods=['DELETE'])
def delete_lessons():
    data = request.get_json()
    if not data or 'ids' not in data:
        return jsonify({"error": "Lesson IDs are required"}), 400

    try:
        lessons = [LessonController.get_by_id(id) for id in data['ids']]
        if None in lessons:
            return jsonify({"error": "Could not find all lessons"}), 404

        for lesson in lessons:
            LessonController.delete(lesson)
        return jsonify(message='Lessons deleted'), 200
    except Exception as e:
        print(f"Error deleting lessons: {e}")
        return jsonify({"error": "Could not delete lessons"}), 500

