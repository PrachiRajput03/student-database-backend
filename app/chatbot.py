import os
from google import genai
from dotenv import load_dotenv

from app.database import SessionLocal
from app import crud, models

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_all_students():
    db = SessionLocal()

    try:
        students = crud.get_students(db)

        return [
            {
                "id": student.id,
                "name": student.name,
                "age": student.age,
                "gender": student.gender,
                "course": student.course,
                "email": student.email
            }
            for student in students
        ]

    finally:
        db.close()


def find_students_by_course(course: str):
    db = SessionLocal()

    try:
        students = db.query(models.Student).filter(
            models.Student.course.ilike(f"%{course}%")
        ).all()

        return [
            {
                "id": student.id,
                "name": student.name,
                "age": student.age,
                "gender": student.gender,
                "course": student.course,
                "email": student.email
            }
            for student in students
        ]

    finally:
        db.close()


def ask_gemini(question: str) -> str:
    students = get_all_students()

    prompt = f"""
You are a student database assistant.

Here is the current student data from the database:

{students}

Answer the user's question using this data.

If the information is not present in the database, clearly say that
you do not have that information.

User question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text