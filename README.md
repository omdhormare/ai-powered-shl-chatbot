# SHL AI-Powered Conversational Assessment Recommender

A production-ready Flask chatbot that helps recruiters discover relevant SHL assessments with conversational memory, follow-up questioning, and ranked top-3 recommendations.

## 1) Architecture
- **Frontend (HTML/CSS/JS):** Chat UI with typing effect + loader.
- **Backend (Flask):** `/chat` endpoint, conversation engine, structured JSON responses.
- **Recommendation Engine:** Hybrid **keyword + semantic (lightweight cosine overlap proxy)** scoring + confidence.
- **Data Layer (JSON):** SHL catalog in `data/assessments.json`.

## 2) Folder Structure
```bash
ai-powered-shl-chatbot/
├── app/
│   ├── __init__.py
│   ├── chat_engine.py
│   ├── config.py
│   ├── recommender.py
│   └── routes.py
├── data/
│   └── assessments.json
├── static/
│   ├── css/styles.css
│   └── js/app.js
├── templates/index.html
├── docs/submission.md
├── requirements.txt
├── render.yaml
├── run.py
├── wsgi.py
└── README.md
```

## 3) Installation
```bash
git clone <your-repo-url>
cd ai-powered-shl-chatbot
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
# production entry: gunicorn wsgi:app
```
Open: `http://127.0.0.1:5000`

## 4) API Docs
### POST `/chat`
Request:
```json
{
  "session_id": "abc-123",
  "message": "Hiring a mid-level Python developer with strong coding and problem-solving"
}
```

Response (recommendation):
```json
{
  "reply": "Great, based on your requirements, here are the top 3 SHL assessments.",
  "intent": "recommend",
  "missing_fields": [],
  "recommendations": [
    {
      "id": "A3",
      "name": "Coding Simulation (JavaScript/Python)",
      "url": "...",
      "confidence": 0.84
    }
  ],
  "conversation_context": {"role":"software developer"},
  "history": []
}
```

### cURL Test
```bash
curl -X POST http://127.0.0.1:5000/chat \
-H "Content-Type: application/json" \
-d '{"session_id":"test1","message":"Hiring junior engineer with python skills"}'
```

## 5) Prompt/Agent Design
- Ask clarifying questions if role/skills/seniority are missing.
- Use only local assessment catalog to reduce hallucinations.
- Return deterministic structured JSON.
- Keep last 12 turns for memory.

## 6) Error Handling
- 400 if `message` missing.
- 500 with safe error payload for unexpected exceptions.

## 7) Deployment Guide
### Render
1. Push code to GitHub.
2. Create new **Web Service** in Render.
3. Connect repo; Render auto-detects `render.yaml`.
4. Deploy.

### Vercel (frontend only optional)
- Deploy static UI independently; point API base URL to Render backend.

## 8) GitHub Upload Commands
```bash
git init
git add .
git commit -m "Initial SHL AI chatbot project"
git branch -M main
git remote add origin <github-repo-url>
git push -u origin main
```

## 9) Sample Screenshots (Description)
- **Home Chat Screen:** Dark modern card UI, chat bubbles, input bar.
- **Recommendation Result:** Bot prints top 3 with confidence scores.
- **Clarification Flow:** Bot asks for missing role/skills/seniority.

## 10) Next Enhancements
- Add OpenAI embeddings for stronger semantic matching.
- Add persistent DB (SQLite/Redis) for multi-instance sessions.
- Add admin panel for catalog updates.
