from models.lesson import Lesson
from db import db
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def create_lesson(grade, lesson_title, learning_objective, user_id):
    # Build prompt based on input
    prompt = f"""
Act as a professional teacher with years of experience in education. Create a detailed lesson plan for students in Grade: {grade}. The lesson's title will be "{lesson_title}", and our primary learning objective is: "{learning_objective}".

Please generate your response strictly in json format. You can use the following json as a template:

{{
  "title": "The title of the lesson",
  "duration": "Estimated time duration of the entire lesson",
  "objective": "The primary learning objective of the lesson",
  "materials": [
    "List of materials needed for the lesson"
  ],
  "sections": [
    {{
      "title": "Title for this section of the lesson",
      "duration": "Estimated duration for this section in minutes",
      "description": "A short description of what this section entails",
      "instructions": "Detailed instructions on how to conduct this section of the lesson"
    }},
    ".... Continue with all necessary sections"
  ],
  "assessment": "How will the understanding of the students be assessed after this lesson",
  "conclusion": "A closing note for the lesson"
}}

The lesson plan should be easy to follow and understand. It should be detailed enough for a substitute teacher to be able to conduct the lesson without any issues. Generate at least 3 sections. The lesson plan should be written in a way that is easy to understand for students in Grade: {grade}.

Only respond with the json so that I may easily convert into an object, nothing else. Do not include this prompt in your response. Do not explain anything, just generate the lesson plan. The lesson plan should be at least 500 words long.

"""


    # Call OpenAI API to generate lesson content
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=1500,
            top_p=1
        )
        lesson_content = response.choices[0].text
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return None

    # Create new lesson object
    lesson = Lesson(grade=grade, lesson_title=lesson_title, learning_objective=learning_objective, content=lesson_content, user_id=user_id)

    # Add new lesson to database
    db.session.add(lesson)
    db.session.commit()

    return lesson
  
  
class LessonController:

    @staticmethod
    def get_by_id(id):
      try:
        lesson = Lesson.query.filter_by(id=id).first()
        if lesson is None:
            return None

        return {
            "id": lesson.id, 
            "grade": lesson.grade, 
            "lesson_title": lesson.lesson_title,
            "learning_objective": lesson.learning_objective,
            "content": lesson.content,
            "date_created": lesson.date_created,
        }
      except Exception as e:
        print(f"Error getting lesson: {e}")
        return None
    
    @staticmethod  
    def get_all():
        try:
            lessons = Lesson.query.all()
            return [
                {
                    "id": lesson.id, 
                    "grade": lesson.grade, 
                    "lesson_title": lesson.lesson_title,
                    "learning_objective": lesson.learning_objective,
                    "content": lesson.content,
                    "date_created": lesson.date_created,
                    "user_id": lesson.user_id
                } 
                for lesson in lessons
            ]
        except Exception as e:
            print(f"Error getting lessons: {e}")
            return None
          
    # Delete lesson by id
    @staticmethod
    def delete_by_id(id):
      try:
        lesson = Lesson.query.filter_by(id=id).first()
        if lesson is None:
            return None

        db.session.delete(lesson)
        db.session.commit()

        return {
            "id": lesson.id, 
            "grade": lesson.grade, 
            "lesson_title": lesson.lesson_title,
            "learning_objective": lesson.learning_objective,
            "content": lesson.content,
            "date_created": lesson.date_created,
        }
      except Exception as e:
        print(f"Error deleting lesson: {e}")
        return None
      
      
      
      
        
      

