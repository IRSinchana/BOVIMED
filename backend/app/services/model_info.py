"""BOVIMED custom YOLO11n model metadata — single source of truth."""

from __future__ import annotations

from typing import Any

from app.config import get_settings

BOVIMED_MODEL_NAME = "BOVIMED YOLO11n"
BOVIMED_MODEL_TYPE = "Custom Object Detection"
BOVIMED_MODEL_FILE = "best.pt"

# Display order for /api/model-info (as specified for BOVIMED training docs)
BOVIMED_CLASSES_DISPLAY = [
    "Cow_drinking_water",
    "Cow_Feeding",
    "Cow_lying",
    "Cow_standing",
    "Healthy_udder",
    "Lumpy_infected_cow",
    "Mastitis_infected_udder",
]

# Official class IDs from backend/models/best.pt (must match trained weights)
BOVIMED_CLASS_NAMES = {
    0: "Cow_Feeding",
    1: "Cow_drinking_water",
    2: "Cow_lying",
    3: "Cow_standing",
    4: "Healthy_udder",
    5: "Lumpy_infected_cow",
    6: "Mastitis_infected_udder",
}

BOVIMED_CLASS_SET = set(BOVIMED_CLASS_NAMES.values()) | set(BOVIMED_CLASSES_DISPLAY)

VALIDATION_METRICS = {
    "mAP50": 0.8454,
    "mAP50_95": 0.6019,
    "precision": 0.8146,
    "recall": 0.7695,
}

SCREENING_DISCLAIMER = (
    "AI-assisted screening. Validation metrics describe model performance on the "
    "validation dataset and do not represent a veterinary diagnosis."
)


def is_valid_bovimed_class(class_name: str) -> bool:
    return str(class_name) in BOVIMED_CLASS_SET


def get_model_metadata(*, model_loaded: bool, demo_mode: bool) -> dict[str, Any]:
    """Compact metadata attached to every analysis response."""
    return {
        "model_name": BOVIMED_MODEL_NAME,
        "model_loaded": bool(model_loaded) and not demo_mode,
        "demo_mode": bool(demo_mode),
    }


def get_model_info() -> dict[str, Any]:
    """Full model transparency payload for GET /api/model-info."""
    from app.services.yolo_service import get_yolo_service

    settings = get_settings()
    yolo = get_yolo_service()
    demo_mode = settings.demo_mode

    model_loaded = False
    if not demo_mode:
        yolo.ensure_model_loaded()
        model_loaded = yolo.model_loaded

    return {
        "model_name": BOVIMED_MODEL_NAME,
        "model_type": BOVIMED_MODEL_TYPE,
        "model_file": BOVIMED_MODEL_FILE,
        "model_loaded": model_loaded,
        "demo_mode": demo_mode,
        "class_count": len(BOVIMED_CLASSES_DISPLAY),
        "classes": list(BOVIMED_CLASSES_DISPLAY),
        "validation_metrics": dict(VALIDATION_METRICS),
    }
