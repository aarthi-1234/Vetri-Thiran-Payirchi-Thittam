from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Any

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    description="AI-powered educational assistant with Q&A, explanations, quizzes, summaries and learning paths.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=30000)


class QARequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=10000)


class QuizRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=500)
    level: str = Field(default="Beginner", max_length=50)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(payload: QARequest) -> dict[str, Any]:
    return {"success": True, "result": answer_question(payload.question)}


@app.post("/explain")
async def explain(payload: TextRequest) -> dict[str, Any]:
    return {"success": True, "result": explain_topic(payload.text)}


@app.post("/quiz")
async def quiz(payload: QuizRequest) -> dict[str, Any]:
    result = generate_quiz(payload.text)
    return {"success": True, **result}


@app.post("/summarize")
async def summarize(payload: TextRequest) -> dict[str, Any]:
    return {"success": True, "result": summarize_text(payload.text)}


@app.post("/learn/recommendations")
async def recommendations(payload: LearningPathRequest) -> dict[str, Any]:
    return {
        "success": True,
        "result": get_learning_recommendations(payload.topic, payload.level),
    }
