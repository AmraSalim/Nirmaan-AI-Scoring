# scoring.py
import math
import pandas as pd
from typing import Dict, Any, List

# Optional NLP tools
try:
    from sentence_transformers import SentenceTransformer, util
    _embed_model = SentenceTransformer("all-MiniLM-L6-v2")
except Exception:
    _embed_model = None

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    _vader = SentimentIntensityAnalyzer()
except Exception:
    _vader = None


class RubricScorer:
    def __init__(self, rubric_path: str = "rubric.csv"):
        self.rubric_df = pd.read_csv(rubric_path)
        self.criteria = self._load_criteria()

    def _load_criteria(self):
        criteria = []
        for _, row in self.rubric_df.iterrows():
            criteria.append({
                "id": row["criterion_id"],
                "name": row["criteria"],
                "metric": row["metric"],
                "description": row.get("details", ""),
                "keywords": [k.strip().lower() for k in str(row.get("keywords", "")).split(",") if k.strip()],
                "weight": float(row["weight"]),
                "min_words": int(row["min_words"]) if not math.isnan(row.get("min_words", math.nan)) else None,
                "max_words": int(row["max_words"]) if not math.isnan(row.get("max_words", math.nan)) else None
            })
        return criteria

    def _keyword_score(self, transcript: str, keywords: List[str]):
        transcript_lower = transcript.lower()
        found = [k for k in keywords if k.lower() in transcript_lower]
        if not keywords:
            return 1.0, []
        return len(found) / len(keywords), found

    def _semantic_score(self, transcript: str, description: str):
        if not _embed_model or not description:
            return 0.5  # fallback
        emb1 = _embed_model.encode(transcript, convert_to_tensor=True)
        emb2 = _embed_model.encode(description, convert_to_tensor=True)
        sim = util.cos_sim(emb1, emb2).item()
        return max(0, min(1, (sim + 1) / 2))  # normalize

    def _length_score(self, transcript: str, min_words: int, max_words: int):
        words = transcript.split()
        count = len(words)
        if not min_words and not max_words:
            return 1.0, count, "Length OK"
        if min_words and count < min_words:
            return 0.3, count, f"Too short (needs ≥ {min_words})"
        if max_words and count > max_words:
            return 0.4, count, f"Too long (limit ≤ {max_words})"
        return 1.0, count, "Length OK"

    def score_transcript(self, transcript: str, duration_sec=None) -> Dict[str, Any]:
        transcript = transcript.strip()
        results = []
        total_weight = sum(c["weight"] for c in self.criteria)
        weighted_sum = 0

        for c in self.criteria:
            kw_score, _ = self._keyword_score(transcript, c["keywords"])
            sem_score = self._semantic_score(transcript, c["description"])
            len_score, _, length_msg = self._length_score(transcript, c["min_words"], c["max_words"])

            # combined score (0–1)
            combined = (0.4 * kw_score) + (0.4 * sem_score) + (0.2 * len_score)
            weighted_sum += combined * c["weight"]

            # only essential fields for output
            results.append({
                "criterion_name": c["name"],
                "metric": c["metric"],
                "score": round(combined * 100, 2),
                "feedback": length_msg
            })

        final_score = round(weighted_sum / total_weight * 100, 2)

        return {
            "overall_score": final_score,
            "word_count": len(transcript.split()),
            "criteria": results
        }
