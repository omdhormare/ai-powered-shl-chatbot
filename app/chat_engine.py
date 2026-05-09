from dataclasses import dataclass, field
from typing import Dict, List

from app.recommender import AssessmentRecommender

REQUIRED_FIELDS = ["role", "skills", "seniority"]


@dataclass
class ConversationState:
    history: List[Dict] = field(default_factory=list)
    context: Dict = field(default_factory=lambda: {
        "role": "",
        "skills": "",
        "seniority": "",
        "industry": "",
        "notes": "",
        "remote_required": True,
    })


class ChatEngine:
    def __init__(self):
        self.recommender = AssessmentRecommender()
        self.sessions: Dict[str, ConversationState] = {}

    def _get_state(self, session_id: str) -> ConversationState:
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationState()
        return self.sessions[session_id]

    def _extract_context(self, message: str, context: Dict) -> None:
        msg = message.lower()
        if "developer" in msg or "engineer" in msg:
            context["role"] = "software developer"
        if any(k in msg for k in ["python", "javascript", "coding", "programming"]):
            context["skills"] = "programming, problem-solving"
        if "entry" in msg or "junior" in msg:
            context["seniority"] = "entry"
        elif "mid" in msg or "3 year" in msg or "4 year" in msg:
            context["seniority"] = "mid"
        elif "senior" in msg or "lead" in msg or "manager" in msg:
            context["seniority"] = "senior"

    def _missing_fields(self, context: Dict) -> List[str]:
        return [k for k in REQUIRED_FIELDS if not context.get(k)]

    def reply(self, session_id: str, message: str) -> Dict:
        state = self._get_state(session_id)
        state.history.append({"role": "user", "content": message})
        self._extract_context(message, state.context)

        missing = self._missing_fields(state.context)
        if missing:
            question = f"I can recommend better assessments if you share: {', '.join(missing)}."
            assistant_reply = {
                "reply": question,
                "intent": "clarify",
                "missing_fields": missing,
                "recommendations": [],
                "conversation_context": state.context,
            }
        else:
            recs = self.recommender.rank(state.context, top_k=3)
            assistant_reply = {
                "reply": "Great, based on your requirements, here are the top 3 SHL assessments.",
                "intent": "recommend",
                "missing_fields": [],
                "recommendations": recs,
                "conversation_context": state.context,
                "hallucination_guardrails": [
                    "Recommendations are selected only from local SHL catalog JSON.",
                    "Unknown requests are handled with clarification questions.",
                ],
            }

        state.history.append({"role": "assistant", "content": assistant_reply["reply"]})
        assistant_reply["history"] = state.history[-12:]
        return assistant_reply
