from sqlalchemy.orm import Session

from app import models, schemas


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(
        name=student.name,
        age=student.age,
        gender=student.gender,
        course=student.course,
        email=student.email
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


def get_students(db: Session):
    return db.query(models.Student).all()


def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()


def update_student(
    db: Session,
    student_id: int,
    student: schemas.StudentCreate
):
    db_student = get_student(db, student_id)

    if db_student is None:
        return None

    db_student.name = student.name
    db_student.age = student.age
    db_student.gender = student.gender
    db_student.course = student.course
    db_student.email = student.email

    db.commit()
    db.refresh(db_student)

    return db_student


def delete_student(db: Session, student_id: int):
    db_student = get_student(db, student_id)

    if db_student is None:
        return None

    db.delete(db_student)
    db.commit()

    return db_student