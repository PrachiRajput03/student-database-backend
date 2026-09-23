from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.vector_store import retrieve_student_context
from app.chatbot import client


class ChatState(TypedDict):
    question: str
    route: str
    context: str
    answer: str


def retrieve_context(state: ChatState):
    context = retrieve_student_context(state["question"])

    return {
        "context": str(context)
    }


def retrieve_database_context(state: ChatState):
    from app.chatbot import get_all_students

    students = get_all_students()

    return {
        "context": str(students)
    }


def route_question(state: ChatState):
    prompt = f"""
You are routing questions for a student database assistant.

Choose exactly ONE of these routes:

DATABASE
Use DATABASE when the question asks for exact structured information,
such as:
- how many students are there
- student with a specific ID
- students in a particular course
- exact student records

VECTOR
Use VECTOR when the question is better answered through semantic
retrieval from student information, such as:
- describe a student
- tell me about a student
- find a student based on a natural-language description
- questions involving descriptive characteristics

Return ONLY one word:
DATABASE
or
VECTOR

Question:
{state["question"]}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    route = response.text.strip().upper()

    if "DATABASE" in route:
        return {"route": "database"}

    return {"route": "vector"}


def choose_retrieval_path(state: ChatState):
    if state["route"] == "database":
        return "database"

    return "vector"


def generate_answer(state: ChatState):
    prompt = f"""
You are a student database assistant.

Use the provided student context to answer the user's question.

Student context:
{state["context"]}

User question:
{state["question"]}

Answer only using the information in the context.
Do not invent student information.
If the context does not contain enough information, say that clearly.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return {
        "answer": response.text
    }


# Create the graph
graph_builder = StateGraph(ChatState)

# Add nodes
graph_builder.add_node("route_question", route_question)
graph_builder.add_node("retrieve_database_context", retrieve_database_context)
graph_builder.add_node("retrieve_context", retrieve_context)
graph_builder.add_node("generate_answer", generate_answer)

# Start → Router
graph_builder.add_edge(START, "route_question")

# Router → appropriate retrieval path
graph_builder.add_conditional_edges(
    "route_question",
    choose_retrieval_path,
    {
        "database": "retrieve_database_context",
        "vector": "retrieve_context"
    }
)

# Both retrieval paths → Gemini
graph_builder.add_edge(
    "retrieve_database_context",
    "generate_answer"
)

graph_builder.add_edge(
    "retrieve_context",
    "generate_answer"
)

# Gemini → End
graph_builder.add_edge("generate_answer", END)

# Compile graph
graph = graph_builder.compile()


if __name__ == "__main__":
    test_state = {
        "question": "Tell me about the female student",
        "route": "",
        "context": "",
        "answer": ""
    }

    print(route_question(test_state))