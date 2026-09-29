from gemini_client import generate_text
from config import USE_LOCAL_EXPLAINER

_local_pipeline = None


def _local_explain(topic: str) -> str:
    global _local_pipeline
    if _local_pipeline is None:
        from transformers import pipeline
        _local_pipeline = pipeline(
            "text2text-generation",
            model="MBZUAI/LaMini-Flan-T5-783M",
        )

    prompt = (
        "Explain the following educational topic for a beginner in simple English. "
        "Use a definition, 3-5 key points, and one simple example.\n\n"
        f"Topic: {topic}"
    )
    result = _local_pipeline(prompt, max_new_tokens=300, do_sample=False)
    return result[0]["generated_text"].strip()


def explain_topic(topic: str) -> str:
    if USE_LOCAL_EXPLAINER:
        try:
            return _local_explain(topic)
        except Exception:
            # Cloud fallback keeps the application usable if the local model
            # cannot be downloaded or loaded on the current machine.
            pass

    prompt = f"""You are EduGenie, an educational tutor.
Explain this topic to a beginner using very simple English.

Topic: {topic}

Format:
1. Simple definition
2. Key points
3. Simple example
4. One-line recap
"""
    return generate_text(prompt)
