# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight AI-powered educational assistant. The project follows the supplied project document's five core functions:

- Ask questions and receive answers
- Explain complex concepts in simple language
- Generate 3-question MCQ quizzes
- Summarize educational text
- Generate a beginner-to-advanced learning path

The backend uses FastAPI and the frontend uses HTML/CSS/JavaScript. Gemini is used for cloud AI generation. The explanation module also contains an optional LaMini-Flan-T5 local-model path.

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── tests/
    └── test_api.py
```

## 1. Prerequisites

Install Python 3.10 or newer.

You also need a Gemini API key. Create one in Google AI Studio and put it in `.env`.

## 2. Open in VS Code

Extract the project ZIP, then open the `EduGenie` folder in VS Code.

Open the integrated terminal:

```powershell
cd path\to\EduGenie
```

## 3. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Configure Gemini

Copy `.env.example` to `.env`.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Open `.env` and replace:

```text
GEMINI_API_KEY=PASTE_YOUR_API_KEY_HERE
```

with your real API key.

Do not upload `.env` to GitHub.

## 6. Run the application

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## 7. Test the application

Run the automated tests:

```bash
pip install pytest
pytest -q
```

The tests mock AI calls, so they do not consume Gemini API quota.

For a real end-to-end test, start the server and try:

### Q&A
Input:
```text
Which is the largest ocean?
```

### Explanation
Input:
```text
Explain the Pythagoras theorem.
```

### Quiz
Input:
```text
Photosynthesis is the process by which green plants use sunlight...
```

The application should return exactly three MCQs with four options each.

### Summary
Paste a long educational paragraph.

### Learning path
Input:
```text
SQL
```

Choose a level and click Generate.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Web interface |
| GET | `/health` | Health check |
| POST | `/qa` | Question answering |
| POST | `/explain` | Concept explanation |
| POST | `/quiz` | 3-question MCQ generation |
| POST | `/summarize` | Educational summarization |
| POST | `/learn/recommendations` | Personalized learning path |

## Example API requests

### Q&A

```json
POST /qa
{
  "question": "What is a database?"
}
```

### Explanation

```json
POST /explain
{
  "text": "Explain inheritance in C++."
}
```

### Quiz

```json
POST /quiz
{
  "text": "A computer network connects devices so they can communicate..."
}
```

### Summary

```json
POST /summarize
{
  "text": "Long educational text..."
}
```

### Learning path

```json
POST /learn/recommendations
{
  "topic": "Python",
  "level": "Beginner"
}
```

## Optional local explanation model

The supplied documentation describes LaMini-Flan-T5-783M for concept explanation. This implementation keeps that option without forcing every student to install a large ML stack.

1. Edit `requirements.txt` and uncomment:

```text
transformers
torch
sentencepiece
```

2. Install them:

```bash
pip install transformers torch sentencepiece
```

3. Change `.env`:

```text
USE_LOCAL_EXPLAINER=true
```

The first local-model run can download model files and may require significant disk space/RAM. If loading fails, the code automatically falls back to Gemini so the application remains usable.

## Troubleshooting

### `GEMINI_API_KEY is missing`

Make sure:
- the file is named exactly `.env`
- `GEMINI_API_KEY=...` is present
- you restarted the server after changing `.env`

### Gemini model error

Change `GEMINI_MODEL` in `.env` to a model currently available to your API key/account. The default is:

```text
gemini-3.8-flash
```

### Port already in use

Run:

```bash
uvicorn main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.

### PowerShell blocks activation

Use:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the virtual environment again.

## Security notes

- Never place the Gemini API key in `index.html` or JavaScript.
- Keep the API key only on the backend in `.env`.
- Do not commit `.env`.
- Add authentication, rate limiting, logging controls and production secret management before public deployment.

## Future enhancements

The supplied project document suggests voice interaction, multilingual support, mobile apps, progress dashboards, gamification, adaptive learning, group study, teacher/parent dashboards, LMS integrations, and image/PDF input as future directions.
