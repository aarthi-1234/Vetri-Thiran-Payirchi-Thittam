from gemini_client import generate_text

def get_learning_recommendations(topic: str, level: str = "Beginner") -> str:
    prompt = f"""Create a structured learning path for the topic "{topic}".
Learner level: {level}

Include:
1. Goal
2. Prerequisites
3. Beginner topics in order
4. Intermediate topics in order
5. Advanced topics in order
6. A realistic suggested timeline
7. Practice activities/projects
8. Recommended resource types (videos, articles, books, documentation)
9. A simple weekly study routine

Keep it practical and easy for a student to follow.
"""
    return generate_text(prompt)
