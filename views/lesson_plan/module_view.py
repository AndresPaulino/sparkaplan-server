# views/lesson_plan/module_view.py
from flask import Blueprint, request, jsonify
import openai
from server.models import db
import server.controllers.ai as ai

module_view = Blueprint("module_view", __name__)

module_types = ['core objective', 'materials', 'warm up', 'instructions', 'guided practice', 'independent practice', 'conclusion']

LESSON_PLAN_PROMPT = """create a {num_minutes} minute lesson plan for {grade} grade students with the following learning objective: {learning_objective}. Make sure to use language that is appropriate for the grade level and subject area.

The response should be formatted as JSON modules each with a title and body, like so: """

LESSON_PLAN_EXAMPLE = """\n[{'title': 'sample module title 1', 'body': 'sample module content 1'}, {'title': 'sample module title 2', 'body': 'sample module body content 2'}}]"""    

SAMPLE_MODULE = {'title': 'sample module title 1', 'body': 'sample module content 1'}

@module_view.route('/<module_id>', methods=['GET'])
def get_module(module_id):
  return db.get_module(module_id)

@module_view.route('/<module_id>/edit', methods=['POST'])
def update_module(module_id):
    data = request.get_json()
    return db.update_module(module_id, data)

@module_view.route('/<module_id>', methods=['DELETE'])
def delete_module(module_id):
  db.delete_module(module_id)
  return jsonify({"success": True}) 

@module_view.route('/<module_id>/regenerate', methods=['POST'])
def regenerate_module(module_id):
  module = db.get_module(module_id)
  lesson_plan = db.get_lesson_plan(module.get("lesson_plan_id"))
  new_module = ai.regenerate_module(lesson_plan, module)
  return db.update_module(module_id, new_module)

@module_view.route('<module_id>/expand', methods=['POST'])
def expand_module(module_id):
  module = db.get_module(module_id)
  lesson_plan = db.get_lesson_plan(module.get("lesson_plan_id"))
  new_module = ai.expand_module(lesson_plan, module)
  return db.update_module(module_id, new_module)