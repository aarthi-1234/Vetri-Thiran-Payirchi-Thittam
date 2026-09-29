from functools import lru_cache
from google import genai
from google.genai import types

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    MAX_OUTPUT_TOKENS,
    TEMPERATURE,
)


class GeminiConfigurationError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client():
    if not GEMINI_API_KEY:
        raise GeminiConfigurationError(
            "GEMINI_API_KEY is missing. Add it to the .env file."
        )
    return genai.Client(api_key=GEMINI_API_KEY)


def generate_text(prompt: str, *, temperature: float | None = None) -> str:
    client = get_client()
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=TEMPERATURE if temperature is None else temperature,
            max_output_tokens=MAX_OUTPUT_TOKENS,
        ),
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
