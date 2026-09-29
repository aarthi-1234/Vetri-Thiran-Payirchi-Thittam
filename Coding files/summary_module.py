from gemini_client import generate_text

def summarize_text(text: str) -> str:
    prompt = f"""Summarize the educational text below for quick revision.

Requirements:
- Keep the important facts.
- Remove repetition.
- Use simple English.
- Prefer short paragraphs and bullet points.
- Do not add information that is not present in the source.

Text:
{text}
"""
    return generate_text(prompt)
