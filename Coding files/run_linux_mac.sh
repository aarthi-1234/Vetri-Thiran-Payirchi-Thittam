#!/usr/bin/env bash
set -e
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if [ ! -f ".env" ]; then cp .env.example .env; fi
echo
echo "EduGenie is ready."
echo "Add your GEMINI_API_KEY to .env, then run:"
echo "uvicorn main:app --reload"
