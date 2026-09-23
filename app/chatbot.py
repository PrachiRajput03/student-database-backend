import os
from google import genai
from dotenv import load_dotenv

from app.database import SessionLocal
from app import crud, models

from app.vector_store import retrieve_student_context

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

def get_student_by_id(student_id: int):
    db = SessionLocal()

    try:
        student = crud.get_student(db, student_id)

        if student is None:
            return {"error": "Student not found"}

        return {
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "gender": student.gender,
            "course": student.course,
            "email": student.email
        }

    finally:
        db.close()

def search_students(
    name: str = None,
    age: int = None,
    gender: str = None,
    course: str = None
):
    db = SessionLocal()

    try:
        query = db.query(models.Student)

        if name:
            query = query.filter(
                models.Student.name.ilike(f"%{name}%")
            )

        if age is not None:
            query = query.filter(models.Student.age == age)

        if gender:
            query = query.filter(
                models.Student.gender.ilike(f"%{gender}%")
            )

        if course:
            query = query.filter(
                models.Student.course.ilike(f"%{course}%")
            )

        students = query.all()

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
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=question,
        config={
    "tools": [
    get_all_students,
    find_students_by_course,
    get_student_by_id,
    search_students
]
}
    )

    return response.text

def ask_gemini_with_context(question: str) -> str:
    context = retrieve_student_context(question)

    prompt = f"""
You are a student database assistant.

Answer the user's question using the student information provided below.

Student information:
{context}

User question:
{question}

If the provided student information does not contain enough information
to answer the question, clearly say that the information is not available.
Do not invent student information.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text