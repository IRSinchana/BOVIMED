"""Recommendation engine — farmer-friendly guidance (no medication prescriptions)."""

from app.services.care_guidance import get_care_guidance


class RecommendationEngine:
    def get_recommendations(self, risk_level: str) -> list[str]:
        care = get_care_guidance(risk_level)
        return list(care["guidance"])


def get_recommendation_engine() -> RecommendationEngine:
    return RecommendationEngine()
