import chromadb

from app.database import SessionLocal
from app import crud



def get_students_for_indexing():
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


# Create a persistent ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db")

# Create or get our student collection
collection = client.get_or_create_collection(
    name="students"
)



def index_students():
    students = get_students_for_indexing()

    if not students:
        return 0

    documents = []
    ids = []
    metadatas = []

    for student in students:
        documents.append(
            f"Student {student['id']}: "
            f"{student['name']} is {student['age']} years old, "
            f"gender {student['gender']}, "
            f"studying {student['course']}, "
            f"email {student['email']}."
        )

        ids.append(str(student["id"]))

        metadatas.append({
            "student_id": student["id"],
            "name": student["name"],
            "course": student["course"]
        })

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    return len(students)


def search_students(query: str, n_results: int = 3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results


def retrieve_student_context(query: str, n_results: int = 3):
    results = search_students(query, n_results)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    context = []

    for document, metadata in zip(documents, metadatas):
        context.append({
            "document": document,
            "student_id": metadata.get("student_id"),
            "name": metadata.get("name"),
            "course": metadata.get("course")
        })

    return context