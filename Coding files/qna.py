from gemini_client import generate_text

SYSTEM = """You are EduGenie, a friendly educational assistant.
Answer the student's question accurately and clearly.
Use simple language suitable for a learner.
Give a direct answer first, then a short explanation when useful.
Do not invent facts. If the question is ambiguous, state the assumption.
"""

def answer_question(question: str) -> str:
    prompt = f"""{SYSTEM}

Student question:
{question}

Answer:"""
    return generate_text(prompt)
