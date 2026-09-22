from pydantic import BaseModel, EmailStr


class StudentCreate(BaseModel):
    name: str
    age: int
    gender: str
    course: str
    email: EmailStr


class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    course: str
    email: EmailStr

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str