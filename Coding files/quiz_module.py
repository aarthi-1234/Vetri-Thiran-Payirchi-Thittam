import json
import re
from typing import Any
from gemini_client import generate_text


def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _fallback_quiz_error(message: str) -> dict[str, Any]:
    return {"quiz": [], "error": message}


def generate_quiz(passage: str) -> dict[str, Any]:
    prompt = f"""Create exactly 3 multiple-choice questions from the educational passage below.

Return ONLY valid JSON. Do not use Markdown fences.
Use this exact structure:
{{
  "quiz": [
    {{
      "question": "Question text",
      "options": ["A", "B", "C", "D"],
      "answer": "A"
    }}
  ]
}}

Rules:
- Exactly 3 questions.
- Exactly 4 options per question.
- "answer" must exactly match one option.
- Questions must be answerable from the passage.
- Make distractors plausible.
- Keep language clear for students.

Passage:
{passage}
"""
    try:
        raw = generate_text(prompt, temperature=0.2)
        data = json.loads(clean_json_block(raw))

        quiz = data.get("quiz")
        if not isinstance(quiz, list) or len(quiz) != 3:
            return _fallback_quiz_error("Gemini returned an invalid quiz format.")

        for item in quiz:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("question"), str)
                or not isinstance(item.get("options"), list)
                or len(item["options"]) != 4
                or item.get("answer") not in item["options"]
            ):
                return _fallback_quiz_error("Gemini returned an invalid quiz item.")

        return {"quiz": quiz}
    except json.JSONDecodeError:
        return _fallback_quiz_error("Could not parse Gemini's quiz JSON response.")
    except Exception as exc:
        return _fallback_quiz_error(str(exc))
