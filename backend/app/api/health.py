from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.schemas import HealthResponse
from app.services.yolo_service import get_yolo_service

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    settings = get_settings()
    yolo = get_yolo_service()
    yolo_status = yolo.status()

    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except Exception:  # noqa: BLE001
        db_status = "error"

    demo = settings.demo_mode
    model_loaded = bool(yolo_status["model_loaded"])
    model_exists = bool(yolo_status["model_exists"])

    if demo:
        message = (
            "Backend healthy. DEMO MODE active - analysis results are clearly labeled "
            "demo/mock. Set DEMO_MODE=false to use backend/models/best.pt."
        )
        status_value = "ok" if db_status == "ok" else "degraded"
    elif model_loaded:
        message = (
            "Backend healthy. Real YOLO11 inference enabled "
            f"({yolo_status['model_path']}). AI-assisted screening only."
        )
        status_value = "ok" if db_status == "ok" else "degraded"
    else:
        message = (
            "Backend running but YOLO11 model is not loaded. "
            f"{yolo_status.get('load_error') or 'Check backend/models/best.pt.'}"
        )
        status_value = "degraded"

    classes = yolo_status.get("class_names") or {}
    model_classes = {str(k): str(v) for k, v in classes.items()}

    return HealthResponse(
        status=status_value,
        service="bovimed-backend",
        demo_mode=demo,
        demo_forced_by_env=settings.demo_mode,
        model_path=yolo_status["model_path"],
        model_exists=model_exists,
        model_loaded=model_loaded,
        model_classes=model_classes,
        load_error=yolo_status.get("load_error"),
        database=db_status,
        message=message,
    )
