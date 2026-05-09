import json
import math
import re
from pathlib import Path
from typing import Dict, List, Tuple


class AssessmentRecommender:
    def __init__(self, data_path: str = "data/assessments.json"):
        self.assessments = self._load_assessments(data_path)

    @staticmethod
    def _load_assessments(data_path: str) -> List[Dict]:
        with Path(data_path).open("r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return re.findall(r"[a-zA-Z0-9+#]+", text.lower())

    def _semantic_score(self, query_tokens: List[str], doc_tokens: List[str]) -> float:
        # Lightweight semantic proxy using token rarity weighting (TF-IDF-like)
        if not query_tokens or not doc_tokens:
            return 0.0
        query_set = set(query_tokens)
        doc_set = set(doc_tokens)
        overlap = query_set.intersection(doc_set)
        if not overlap:
            return 0.0
        return len(overlap) / math.sqrt(len(query_set) * len(doc_set))

    def rank(self, hiring_context: Dict, top_k: int = 3) -> List[Dict]:
        query = " ".join([
            hiring_context.get("role", ""),
            hiring_context.get("skills", ""),
            hiring_context.get("seniority", ""),
            hiring_context.get("industry", ""),
            hiring_context.get("notes", ""),
        ])
        query_tokens = self._tokenize(query)

        ranked: List[Tuple[float, Dict]] = []
        for assessment in self.assessments:
            corpus = " ".join([
                assessment["name"],
                assessment["description"],
                " ".join(assessment.get("skills", [])),
                " ".join(assessment.get("keywords", [])),
                " ".join(assessment.get("job_levels", [])),
            ])
            doc_tokens = self._tokenize(corpus)

            semantic = self._semantic_score(query_tokens, doc_tokens)
            keyword_hits = len(set(query_tokens).intersection(set(doc_tokens)))
            keyword_score = min(keyword_hits / 10.0, 1.0)

            seniority_boost = 0.15 if hiring_context.get("seniority", "").lower() in assessment.get("job_levels", []) else 0.0
            remote_boost = 0.05 if hiring_context.get("remote_required", True) and assessment.get("remote_testing") else 0.0

            score = 0.5 * semantic + 0.3 * keyword_score + seniority_boost + remote_boost
            confidence = round(min(score, 0.99), 2)

            ranked.append((score, {
                "id": assessment["id"],
                "name": assessment["name"],
                "url": assessment["url"],
                "duration_minutes": assessment["duration_minutes"],
                "remote_testing": assessment["remote_testing"],
                "adaptive": assessment["adaptive"],
                "confidence": confidence,
                "match_reasons": [
                    f"Keyword overlap: {keyword_hits}",
                    f"Semantic similarity: {round(semantic, 2)}",
                ],
            }))

        ranked.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in ranked[:top_k]]
