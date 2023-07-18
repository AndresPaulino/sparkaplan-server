from models.lesson import Lesson
from db import db
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def create_lesson(grade, lesson_title, learning_objective, user_id):
    # Build prompt based on input
    prompt = f"Grade: {grade}\nLesson Title: {lesson_title}\nLearning Objective: {learning_objective}\nGenerate a lesson plan:"

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
