# Student Database Application System – Backend

A modular backend application for managing student records and providing an AI-powered chatbot for querying student information.

## Features

* Student CRUD operations
* REST APIs using FastAPI
* SQLite database with SQLAlchemy ORM
* Interactive API documentation with Swagger UI
* Gemini API integration
* AI-powered student database chatbot
* ChromaDB for semantic student information retrieval
* LangGraph-based routing and chatbot workflow
* Database retrieval for structured queries
* Vector retrieval for natural-language queries

## Technologies Used

* Python
* FastAPI
* SQLite
* SQLAlchemy
* Pydantic
* Google Gemini API
* ChromaDB
* LangGraph
* Uvicorn

## Project Structure

```text
student-database-backend/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── chatbot.py
│   ├── vector_store.py
│   └── graph.py
│
├── requirements.txt
├── .gitignore
├── README.md
└── .env
```

## API Endpoints

### Student APIs

| Method | Endpoint                 | Description         |
| ------ | ------------------------ | ------------------- |
| POST   | `/students`              | Create a student    |
| GET    | `/students`              | Get all students    |
| GET    | `/students/{student_id}` | Get a student by ID |
| PUT    | `/students/{student_id}` | Update a student    |
| DELETE | `/students/{student_id}` | Delete a student    |

### Chatbot API

| Method | Endpoint | Description                              |
| ------ | -------- | ---------------------------------------- |
| POST   | `/chat`  | Ask a question about student information |

## AI Chatbot Workflow

The chatbot uses LangGraph to route questions to the appropriate retrieval method.

```text
User Question
      │
      ▼
  FastAPI /chat
      │
      ▼
  LangGraph Router
      │
      ├───────────────┐
      ▼               ▼
  DATABASE          VECTOR
      │               │
      ▼               ▼
   SQLite          ChromaDB
      │               │
      └───────┬───────┘
              ▼
          Gemini API
              │
              ▼
          Final Answer
```

### Database Route

Structured questions such as:

* How many students are currently in the database?
* Which students are studying MCA?
* What is the email of student 1?
* List all students.

are routed to the database retrieval path.

### Vector Route

Natural-language or descriptive questions such as:

* Tell me about the female student.
* What do you know about the student who is 22 years old?

are routed through ChromaDB for semantic retrieval.

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd student-database-backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Git Bash:

```bash
source venv/Scripts/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Do not commit the `.env` file to GitHub.

### 6. Start the application

```bash
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

## Swagger Documentation

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

The Swagger interface can be used to test the student CRUD APIs and the chatbot endpoint.

## Example Chat Request

```json
{
  "question": "How many students are currently in the database?"
}
```

Example response:

```json
{
  "answer": "There is currently 1 student in the database."
}
```

## Notes

* The SQLite database is created locally when the application is run.
* ChromaDB data is generated locally and is not committed to the repository.
* API credentials are stored in environment variables and should not be committed.
