"""YOLO11 detection service for BOVIMED custom weights."""

from __future__ import annotations

import logging
import threading
from dataclasses import dataclass, field

import cv2
import numpy as np
from fastapi import HTTPException, status

from app.config import Settings, get_settings

logger = logging.getLogger(__name__)

# Official BOVIMED trained class names (must match best.pt)
BOVIMED_CLASS_NAMES = {
    0: "Cow_Feeding",
    1: "Cow_drinking_water",
    2: "Cow_lying",
    3: "Cow_standing",
    4: "Healthy_udder",
    5: "Lumpy_infected_cow",
    6: "Mastitis_infected_udder",
}

HEALTH_RELEVANT_CLASSES = {
    "Healthy_udder",
    "Lumpy_infected_cow",
    "Mastitis_infected_udder",
}


@dataclass
class InferenceResult:
    detections: list[dict] = field(default_factory=list)
    primary_finding: dict | None = None
    annotated_image: np.ndarray | None = None
    demo_mode: bool = False
    model_version: str = ""
    message: str = ""
    class_names: dict = field(default_factory=dict)


class YOLODetectionService:
    """
    Loads Ultralytics YOLO11 from backend/models/best.pt.

    DEMO_MODE=true → clearly labeled mock results (dev only).
    DEMO_MODE=false → real inference; errors if weights missing/unloadable.
    Never silently fabricates detections as real results.
    """

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self._model = None
        self._load_error: str | None = None
        self._lock = threading.Lock()
        self._attempted_load = False

    @property
    def model_exists(self) -> bool:
        path = self.settings.resolved_model_path
        return path.is_file() and path.stat().st_size > 0

    @property
    def model_loaded(self) -> bool:
        return self._model is not None

    @property
    def using_demo(self) -> bool:
        return bool(self.settings.demo_mode)

    def ensure_model_loaded(self) -> None:
        if self.using_demo:
            return
        if self._model is not None:
            return
        with self._lock:
            if self._model is not None:
                return
            self._attempted_load = True
            model_path = self.settings.resolved_model_path

            if not model_path.is_file():
                self._load_error = (
                    f"Model file not found at {model_path}. "
                    "Place trained weights at backend/models/best.pt"
                )
                logger.error(self._load_error)
                return

            if model_path.stat().st_size == 0:
                self._load_error = f"Model file is empty: {model_path}"
                logger.error(self._load_error)
                return

            try:
                from ultralytics import YOLO

                logger.info("Loading YOLO11 model from %s", model_path)
                self._model = YOLO(str(model_path))
                self._load_error = None
                names = getattr(self._model, "names", None) or {}
                logger.info("YOLO11 loaded successfully | classes=%s", names)
            except Exception as exc:  # noqa: BLE001
                self._model = None
                self._load_error = str(exc)
                logger.exception("Failed to load YOLO model from %s", model_path)

    def predict(self, image_bgr: np.ndarray) -> InferenceResult:
        if self.using_demo:
            return self._demo_inference(
                image_bgr,
                "DEMO_MODE=true in environment",
            )

        self.ensure_model_loaded()
        if self._model is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=(
                    "YOLO11 model could not be loaded. "
                    f"{self._load_error or 'Unknown load error.'} "
                    "Ensure backend/models/best.pt exists, or set DEMO_MODE=true for labeled demo results."
                ),
            )

        try:
            return self._real_inference(image_bgr)
        except HTTPException:
            raise
        except Exception as exc:  # noqa: BLE001
            logger.exception("YOLO inference failed")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=(
                    "YOLO11 inference failed while processing the image. "
                    "Please try again with another image."
                ),
            ) from exc

    def _real_inference(self, image_bgr: np.ndarray) -> InferenceResult:
        results = self._model.predict(source=image_bgr, verbose=False)
        detections: list[dict] = []
        annotated = image_bgr.copy()
        names = dict(getattr(self._model, "names", None) or BOVIMED_CLASS_NAMES)

        if results:
            result = results[0]
            names = dict(result.names or names)
            if result.boxes is not None and len(result.boxes) > 0:
                for box in result.boxes:
                    cls_id = int(box.cls.item()) if box.cls is not None else -1
                    conf = float(box.conf.item()) if box.conf is not None else 0.0
                    class_name = str(names.get(cls_id, f"class_{cls_id}"))
                    xyxy = box.xyxy[0].tolist() if box.xyxy is not None else None
                    detections.append(
                        {
                            "class_id": cls_id,
                            "class_name": class_name,
                            "confidence": conf,
                            "bbox": [float(v) for v in xyxy] if xyxy else None,
                        }
                    )
            try:
                plotted = result.plot()
                if plotted is not None:
                    annotated = plotted
            except Exception:  # noqa: BLE001
                annotated = self._draw_boxes(image_bgr, detections)

        primary = self._select_primary_finding(detections)
        if detections:
            message = (
                "REAL MODEL RESULT - YOLO11 inference completed. "
                "AI-assisted screening result only; not a veterinary diagnosis."
            )
        else:
            message = (
                "REAL MODEL RESULT - no objects detected by YOLO11. "
                "AI-assisted screening result only; not a veterinary diagnosis."
            )

        return InferenceResult(
            detections=detections,
            primary_finding=primary,
            annotated_image=annotated,
            demo_mode=False,
            model_version=self.settings.model_version,
            message=message,
            class_names=names,
        )

    @staticmethod
    def _select_primary_finding(detections: list[dict]) -> dict | None:
        """Prefer mastitis, then lumpy, then healthy_udder, else highest confidence."""
        if not detections:
            return None

        priority = {
            "Mastitis_infected_udder": 300,
            "Lumpy_infected_cow": 200,
            "Healthy_udder": 100,
        }

        def sort_key(det: dict) -> tuple:
            name = str(det.get("class_name", ""))
            return (
                priority.get(name, 0),
                float(det.get("confidence", 0.0)),
            )

        return max(detections, key=sort_key)

    def _demo_inference(self, image_bgr: np.ndarray, reason: str) -> InferenceResult:
        h, w = image_bgr.shape[:2]
        cx, cy = w // 2, h // 2
        bw, bh = max(40, w // 5), max(40, h // 5)
        bbox = [
            float(cx - bw // 2),
            float(cy - bh // 2),
            float(cx + bw // 2),
            float(cy + bh // 2),
        ]
        detections = [
            {
                "class_id": 6,
                "class_name": "Mastitis_infected_udder",
                "confidence": 0.82,
                "bbox": bbox,
            }
        ]
        annotated = self._draw_boxes(image_bgr, detections, label_prefix="DEMO")
        cv2.putText(
            annotated,
            "DEMO MODE - NOT A REAL MODEL RESULT",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )
        return InferenceResult(
            detections=detections,
            primary_finding=detections[0],
            annotated_image=annotated,
            demo_mode=True,
            model_version=f"{self.settings.model_version}-demo",
            message=f"DEMO/MOCK RESULT - {reason}",
            class_names=dict(BOVIMED_CLASS_NAMES),
        )

    @staticmethod
    def _draw_boxes(
        image_bgr: np.ndarray,
        detections: list[dict],
        label_prefix: str | None = None,
    ) -> np.ndarray:
        out = image_bgr.copy()
        for det in detections:
            bbox = det.get("bbox")
            if not bbox or len(bbox) != 4:
                continue
            x1, y1, x2, y2 = [int(v) for v in bbox]
            color = (0, 140, 255) if label_prefix == "DEMO" else (40, 180, 80)
            cv2.rectangle(out, (x1, y1), (x2, y2), color, 2)
            name = det.get("class_name", "object")
            conf = float(det.get("confidence", 0.0))
            label = f"{label_prefix + ': ' if label_prefix else ''}{name} {conf:.1%}"
            cv2.putText(
                out,
                label,
                (x1, max(20, y1 - 8)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                color,
                2,
                cv2.LINE_AA,
            )
        return out

    def status(self) -> dict:
        path = self.settings.resolved_model_path
        if not self.using_demo:
            self.ensure_model_loaded()
        return {
            "demo_mode": self.using_demo or (not self.model_loaded and self.settings.demo_mode),
            "demo_forced_by_env": self.settings.demo_mode,
            "model_path": str(path),
            "model_exists": self.model_exists,
            "model_loaded": self.model_loaded,
            "load_error": self._load_error,
            "class_names": dict(getattr(self._model, "names", None) or {})
            if self._model is not None
            else dict(BOVIMED_CLASS_NAMES),
        }


_yolo_service: YOLODetectionService | None = None


def get_yolo_service() -> YOLODetectionService:
    global _yolo_service
    if _yolo_service is None:
        _yolo_service = YOLODetectionService()
    return _yolo_service


def reset_yolo_service() -> None:
    """Test/helper hook to reload model after env changes."""
    global _yolo_service
    _yolo_service = None
