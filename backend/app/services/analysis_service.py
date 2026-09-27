"""Orchestrates analysis: image → YOLO → risk → recommendations → persistence."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.config import get_settings
from app.models import Alert, Analysis, Cow, Detection
from app.schemas import AnalysisOut, DetectionOut, PrimaryFindingOut
from app.services.image_service import ImageService, get_image_service
from app.services.recommendation_engine import (
    RecommendationEngine,
    get_recommendation_engine,
)
from app.services.risk_engine import RiskEngine, get_risk_engine
from app.services.model_info import BOVIMED_MODEL_NAME, get_model_metadata, is_valid_bovimed_class
from app.services.yolo_service import YOLODetectionService, get_yolo_service

logger = logging.getLogger(__name__)


class AnalysisService:
    def __init__(
        self,
        db: Session,
        image_service: ImageService | None = None,
        yolo_service: YOLODetectionService | None = None,
        risk_engine: RiskEngine | None = None,
        recommendation_engine: RecommendationEngine | None = None,
    ):
        self.db = db
        self.images = image_service or get_image_service()
        self.yolo = yolo_service or get_yolo_service()
        self.risk = risk_engine or get_risk_engine()
        self.recommendations = recommendation_engine or get_recommendation_engine()
        self.settings = get_settings()

    async def analyze(
        self,
        file: UploadFile,
        cow_id: str | None = None,
        user_id: int | None = None,
    ) -> AnalysisOut:
        data, ext, _fmt = await self.images.read_and_validate(file)
        image_bgr = self.images.preprocess(data)
        upload_path = self.images.save_upload(image_bgr, ext)

        inference = self.yolo.predict(image_bgr)
        for det in inference.detections:
            class_name = str(det.get("class_name", ""))
            if class_name and not is_valid_bovimed_class(class_name):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=(
                        f"Unexpected detection class '{class_name}' from model. "
                        "Only BOVIMED YOLO11n trained classes are accepted."
                    ),
                )
        logger.info(
            "Model: %s | Model loaded: %s | Demo mode: %s | Detections: %s",
            BOVIMED_MODEL_NAME,
            (not inference.demo_mode) and self.yolo.model_loaded,
            inference.demo_mode,
            len(inference.detections),
        )
        risk = self.risk.assess(
            inference.detections,
            demo_mode=inference.demo_mode,
            primary_finding=inference.primary_finding,
        )
        recs = self.recommendations.get_recommendations(risk.risk_level)

        # Confidence shown to users: primary finding conf if present, else risk score
        display_confidence = risk.score
        if risk.primary_finding and risk.relevant_detections:
            display_confidence = float(risk.primary_finding.get("confidence", risk.score))

        annotated_path = None
        if inference.annotated_image is not None:
            annotated_path = self.images.save_annotated(
                inference.annotated_image,
                stem=upload_path.stem,
            )

        resolved_cow_id = self._ensure_cow(cow_id)

        try:
            analysis = Analysis(
                cow_id=resolved_cow_id,
                image_path=str(upload_path),
                annotated_image_path=str(annotated_path) if annotated_path else None,
                prediction=risk.prediction,
                confidence=display_confidence,
                risk_level=risk.risk_level,
                recommendations=recs,
                model_version=inference.model_version,
                demo_mode=inference.demo_mode,
                notes=inference.message,
                timestamp=datetime.now(timezone.utc),
            )
            self.db.add(analysis)
            self.db.flush()

            for det in inference.detections:
                bbox = det.get("bbox") or [None, None, None, None]
                self.db.add(
                    Detection(
                        analysis_id=analysis.id,
                        class_name=str(det.get("class_name", "unknown")),
                        confidence=float(det.get("confidence", 0.0)),
                        bbox_x1=bbox[0] if bbox and len(bbox) > 0 else None,
                        bbox_y1=bbox[1] if bbox and len(bbox) > 1 else None,
                        bbox_x2=bbox[2] if bbox and len(bbox) > 2 else None,
                        bbox_y2=bbox[3] if bbox and len(bbox) > 3 else None,
                    )
                )

            if risk.risk_level in (
                RiskEngine.MILD,
                RiskEngine.MODERATE,
                RiskEngine.HIGH,
                RiskEngine.CRITICAL,
                "Severe",  # legacy
            ):
                self.db.add(
                    self._build_alert(analysis, risk.risk_level, display_confidence)
                )

            self.db.commit()
            analysis = self.db.scalar(
                select(Analysis)
                .options(selectinload(Analysis.detections))
                .where(Analysis.id == analysis.id)
            )

            if not inference.demo_mode and risk.risk_level in (
                RiskEngine.MILD,
                RiskEngine.MODERATE,
                RiskEngine.HIGH,
                RiskEngine.CRITICAL,
                "Severe",
            ):
                from app.services.notification_service import create_analysis_notifications

                try:
                    create_analysis_notifications(
                        self.db,
                        analysis,
                        user_id=user_id,
                    )
                except Exception:  # noqa: BLE001
                    logger.exception("Failed to create health notifications for analysis %s", analysis.id)
        except Exception as exc:  # noqa: BLE001
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database failure while saving analysis. Please try again.",
            ) from exc

        return self.to_analysis_out(
            analysis,
            risk_explanation=risk.explanation,
            primary_finding=risk.primary_finding,
            inference_detections=inference.detections,
        )

    def _ensure_cow(self, cow_id: str | None) -> str:
        if cow_id:
            cow_id = cow_id.strip()
            existing = self.db.scalar(select(Cow).where(Cow.cow_id == cow_id))
            if existing:
                return existing.cow_id
            cow = Cow(cow_id=cow_id, name=cow_id)
            self.db.add(cow)
            self.db.flush()
            return cow.cow_id

        count = self.db.scalar(select(func.count()).select_from(Cow)) or 0
        for i in range(count + 1, count + 1000):
            candidate = f"COW-{i:03d}"
            exists = self.db.scalar(select(Cow).where(Cow.cow_id == candidate))
            if not exists:
                self.db.add(Cow(cow_id=candidate, name=candidate))
                self.db.flush()
                return candidate
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not allocate a new cow ID.",
        )

    @staticmethod
    def _build_alert(analysis: Analysis, risk_level: str, confidence: float) -> Alert:
        from app.services.care_guidance import get_care_guidance, normalize_risk

        level = normalize_risk(risk_level)
        care = get_care_guidance(level)
        severity = {
            "Mild": "info",
            "Moderate": "warning",
            "High": "high",
            "Critical": "critical",
        }.get(level, "warning")
        message = (
            f"Cow {analysis.cow_id}: {analysis.prediction}. "
            f"Risk: {level}. AI Confidence: {confidence:.1%}. "
            f"{care['next_step']} Not a veterinary diagnosis."
        )
        return Alert(
            analysis_id=analysis.id,
            cow_id=analysis.cow_id,
            severity=severity,
            title=care["title"],
            message=message,
            risk_level=level,
            confidence=confidence,
            is_read=False,
        )

    def to_analysis_out(
        self,
        analysis: Analysis,
        risk_explanation: str | None = None,
        primary_finding: dict | None = None,
        inference_detections: list[dict] | None = None,
    ) -> AnalysisOut:
        detections_out: list[DetectionOut] = []
        class_id_by_name_conf: dict[tuple, int | None] = {}
        if inference_detections:
            for det in inference_detections:
                key = (
                    str(det.get("class_name")),
                    round(float(det.get("confidence", 0.0)), 6),
                )
                class_id_by_name_conf[key] = det.get("class_id")

        for det in getattr(analysis, "detections", []) or []:
            bbox = None
            if None not in (det.bbox_x1, det.bbox_y1, det.bbox_x2, det.bbox_y2):
                bbox = [det.bbox_x1, det.bbox_y1, det.bbox_x2, det.bbox_y2]
            class_id = class_id_by_name_conf.get(
                (det.class_name, round(float(det.confidence), 6))
            )
            detections_out.append(
                DetectionOut(
                    id=det.id,
                    class_id=class_id,
                    class_name=det.class_name,
                    confidence=det.confidence,
                    bbox=bbox,
                )
            )

        primary_out = None
        if primary_finding:
            primary_out = PrimaryFindingOut(
                class_id=primary_finding.get("class_id"),
                class_name=str(primary_finding.get("class_name")),
                confidence=float(primary_finding.get("confidence", 0.0)),
                bbox=primary_finding.get("bbox"),
            )
        elif detections_out:
            # Fallback: highest-confidence stored detection
            top = max(detections_out, key=lambda d: d.confidence)
            primary_out = PrimaryFindingOut(
                class_id=top.class_id,
                class_name=top.class_name,
                confidence=top.confidence,
                bbox=top.bbox,
            )

        from app.services.care_guidance import get_care_guidance

        model_meta = get_model_metadata(
            model_loaded=self.yolo.model_loaded,
            demo_mode=analysis.demo_mode,
        )

        image_url = self.images.to_public_url(analysis.image_path, "uploads")
        annotated_image_url = self.images.to_public_url(
            analysis.annotated_image_path, "results"
        )
        if image_url and not self.images.media_file_exists(analysis.image_path, "uploads"):
            logger.warning(
                "Upload image missing on disk for analysis %s: %s",
                analysis.id,
                analysis.image_path,
            )
        if annotated_image_url and not self.images.media_file_exists(
            analysis.annotated_image_path, "results"
        ):
            logger.warning(
                "Annotated image missing on disk for analysis %s: %s",
                analysis.id,
                analysis.annotated_image_path,
            )

        return AnalysisOut(
            success=True,
            analysis_id=analysis.id,
            cow_id=analysis.cow_id,
            prediction=analysis.prediction,
            confidence=analysis.confidence,
            risk_level=analysis.risk_level,
            detections=detections_out,
            primary_finding=primary_out,
            recommendations=list(analysis.recommendations or []),
            timestamp=analysis.timestamp,
            model_version=analysis.model_version,
            model_name=model_meta["model_name"],
            model_loaded=model_meta["model_loaded"],
            demo_mode=analysis.demo_mode,
            image_url=image_url,
            annotated_image_url=annotated_image_url,
            risk_explanation=risk_explanation or analysis.notes,
            screening_type="AI-assisted screening result",
            care_guidance=get_care_guidance(analysis.risk_level),
        )

    def get_analysis(self, analysis_id: int) -> Analysis:
        analysis = self.db.scalar(
            select(Analysis)
            .options(selectinload(Analysis.detections))
            .where(Analysis.id == analysis_id)
        )
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Analysis {analysis_id} not found.",
            )
        return analysis
