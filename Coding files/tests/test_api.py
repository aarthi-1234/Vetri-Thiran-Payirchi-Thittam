from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_qa(monkeypatch):
    monkeypatch.setattr(main, "answer_question", lambda q: "The Pacific Ocean is the largest ocean.")
    response = client.post("/qa", json={"question": "Which is the largest ocean?"})
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_explain(monkeypatch):
    monkeypatch.setattr(main, "explain_topic", lambda t: "Simple explanation")
    response = client.post("/explain", json={"text": "Photosynthesis"})
    assert response.status_code == 200


def test_summary(monkeypatch):
    monkeypatch.setattr(main, "summarize_text", lambda t: "Short summary")
    response = client.post("/summarize", json={"text": "A long educational passage."})
    assert response.status_code == 200


def test_learning_path(monkeypatch):
    monkeypatch.setattr(main, "get_learning_recommendations", lambda t, l: "Learning path")
    response = client.post(
        "/learn/recommendations",
        json={"topic": "SQL", "level": "Beginner"},
    )
    assert response.status_code == 200


def test_quiz(monkeypatch):
    sample = {
        "quiz": [
            {"question": "2+2?", "options": ["1", "2", "3", "4"], "answer": "4"},
            {"question": "Capital of India?", "options": ["Delhi", "Paris", "Rome", "Tokyo"], "answer": "Delhi"},
            {"question": "Water formula?", "options": ["CO2", "H2O", "O2", "NaCl"], "answer": "H2O"},
        ]
    }
    monkeypatch.setattr(main, "generate_quiz", lambda t: sample)
    response = client.post("/quiz", json={"text": "Basic facts"})
    assert response.status_code == 200
    assert len(response.json()["quiz"]) == 3
