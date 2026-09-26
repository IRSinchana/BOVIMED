"""Risk assessment engine — BOVIMED class-aware interpretation of detections."""

from __future__ import annotations

from dataclasses import dataclass

from app.config import Settings, get_settings
from app.services.yolo_service import HEALTH_RELEVANT_CLASSES


@dataclass(frozen=True)
class RiskResult:
    risk_level: str
    score: float
    explanation: str
    prediction: str
    primary_finding: dict | None = None
    relevant_detections: tuple = ()


class RiskEngine:
    """
    Application-level interpretation of YOLO detections.

    Thresholds come from environment variables.
    This is AI-assisted screening only — not a veterinary diagnosis.
    """

    LOW = "Low"
    MILD = "Mild"
    MODERATE = "Moderate"
    HIGH = "High"
    CRITICAL = "Critical"

    # Legacy aliases kept for older DB rows / comparisons
    HEALTHY = LOW
    SEVERE = HIGH

    MASTITIS = "Mastitis_infected_udder"
    LUMPY = "Lumpy_infected_cow"
    HEALTHY_UDDER = "Healthy_udder"

    BEHAVIORAL_CLASSES = {
        "Cow_Feeding",
        "Cow_drinking_water",
        "Cow_lying",
        "Cow_standing",
    }

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()

    def assess(
        self,
        detections: list[dict],
        *,
        demo_mode: bool = False,
        primary_finding: dict | None = None,
    ) -> RiskResult:
        relevant = [
            d
            for d in detections
            if str(d.get("class_name", "")) in HEALTH_RELEVANT_CLASSES
        ]
        primary = primary_finding or self._pick_primary(relevant or detections)

        if not relevant:
            prediction = (
                "No Relevant Health Detection"
                if detections
                else "No Detection"
            )
            explanation = self._build_explanation(
                score=0.0,
                risk_level=self.LOW,
                detections=detections,
                relevant=relevant,
                demo_mode=demo_mode,
                extra=(
                    "No Healthy_udder, Lumpy_infected_cow, or Mastitis_infected_udder "
                    "finding was returned by the model. Behavioral detections alone "
                    "are not treated as mastitis risk."
                    if detections
                    else "The model returned no detections for this image."
                ),
            )
            return RiskResult(
                risk_level=self.LOW,
                score=0.0,
                explanation=explanation,
                prediction=prediction,
                primary_finding=primary,
                relevant_detections=tuple(relevant),
            )

        score = self._compute_score(relevant)
        risk_level = self._score_to_level(score, relevant)
        prediction = self._prediction_label(relevant, primary)
        explanation = self._build_explanation(
            score=score,
            risk_level=risk_level,
            detections=detections,
            relevant=relevant,
            demo_mode=demo_mode,
        )
        return RiskResult(
            risk_level=risk_level,
            score=round(score, 4),
            explanation=explanation,
            prediction=prediction,
            primary_finding=primary,
            relevant_detections=tuple(relevant),
        )

    def _pick_primary(self, detections: list[dict]) -> dict | None:
        if not detections:
            return None
        priority = {
            self.MASTITIS: 300,
            self.LUMPY: 200,
            self.HEALTHY_UDDER: 100,
        }

        def key(det: dict) -> tuple:
            return (
                priority.get(str(det.get("class_name", "")), 0),
                float(det.get("confidence", 0.0)),
            )

        return max(detections, key=key)

    def _compute_score(self, relevant: list[dict]) -> float:
        """
        Map health-relevant detections to an application risk score.

        - Mastitis_infected_udder: primary mastitis signal (full confidence)
        - Lumpy_infected_cow: infection-related signal (0.85x confidence)
        - Healthy_udder: reduces risk (inverse of confidence)
        """
        mastitis = [
            float(d["confidence"])
            for d in relevant
            if d.get("class_name") == self.MASTITIS
        ]
        lumpy = [
            float(d["confidence"])
            for d in relevant
            if d.get("class_name") == self.LUMPY
        ]
        healthy = [
            float(d["confidence"])
            for d in relevant
            if d.get("class_name") == self.HEALTHY_UDDER
        ]

        if mastitis:
            top = max(mastitis)
            avg = sum(mastitis) / len(mastitis)
            return min(1.0, (0.75 * top) + (0.25 * avg))

        if lumpy:
            top = max(lumpy)
            return min(1.0, top * 0.85)

        if healthy:
            # Strong healthy_udder detection → low risk score
            return max(0.0, 1.0 - max(healthy))

        return 0.0

    def _score_to_level(self, score: float, relevant: list[dict] | None = None) -> str:
        s = self.settings
        has_mastitis = any(
            d.get("class_name") == self.MASTITIS for d in (relevant or [])
        )
        # Critical: very high score with mastitis signal
        if score >= max(s.severe_threshold, 0.92) and has_mastitis:
            return self.CRITICAL
        if score >= s.severe_threshold:
            return self.HIGH
        if score >= s.moderate_threshold:
            return self.MODERATE
        if score >= s.mild_threshold:
            return self.MILD
        if score >= s.healthy_threshold:
            return self.MILD
        return self.LOW

    def _prediction_label(
        self,
        relevant: list[dict],
        primary: dict | None,
    ) -> str:
        names = {str(d.get("class_name", "")) for d in relevant}
        if self.MASTITIS in names:
            return "Possible signs of udder infection detected"
        if self.LUMPY in names:
            return "Possible infection-related signs detected"
        if self.HEALTHY_UDDER in names:
            return "Healthy udder signs detected"
        return "AI screening complete"

    def _build_explanation(
        self,
        score: float,
        risk_level: str,
        detections: list[dict],
        relevant: list[dict],
        demo_mode: bool,
        extra: str = "",
    ) -> str:
        s = self.settings
        mode_note = (
            " [DEMO MODE - not a real model inference.]"
            if demo_mode
            else ""
        )
        parts = [
            f"AI-assisted screening result.{mode_note}",
            (
                f"Risk score {score:.1%} mapped using thresholds "
                f"(Healthy < {s.healthy_threshold:.0%}, "
                f"Mild ≥ {s.mild_threshold:.0%}, "
                f"Moderate ≥ {s.moderate_threshold:.0%}, "
                f"Severe ≥ {s.severe_threshold:.0%})."
            ),
            f"Assessed level: {risk_level}.",
            f"Total detections: {len(detections)}; health-relevant: {len(relevant)}.",
            "This is not a veterinary diagnosis. Veterinary confirmation is recommended.",
        ]
        if extra:
            parts.insert(1, extra)
        return " ".join(parts)


def get_risk_engine() -> RiskEngine:
    return RiskEngine()
