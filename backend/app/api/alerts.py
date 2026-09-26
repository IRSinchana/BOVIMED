from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models import Alert, Analysis, Cow
from app.services.care_guidance import get_care_guidance, normalize_risk

router = APIRouter(tags=["Alerts"])


@router.get("/alerts")
def list_alerts(
    unread_only: bool = Query(default=False),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    stmt = select(Alert).order_by(Alert.created_at.desc()).limit(limit)
    if unread_only:
        stmt = (
            select(Alert)
            .where(Alert.is_read.is_(False))
            .order_by(Alert.created_at.desc())
            .limit(limit)
        )
    alerts = db.scalars(stmt).all()
    out = []
    for a in alerts:
        analysis = db.scalar(
            select(Analysis)
            .options(selectinload(Analysis.detections))
            .where(Analysis.id == a.analysis_id)
        )
        cow = db.scalar(select(Cow).where(Cow.cow_id == a.cow_id))
        level = normalize_risk(a.risk_level)
        care = get_care_guidance(level)
        detections = []
        primary_class = None
        if analysis:
            for d in analysis.detections or []:
                detections.append(
                    {
                        "class_name": d.class_name,
                        "confidence": d.confidence,
                    }
                )
            if detections:
                primary_class = max(detections, key=lambda x: x["confidence"])["class_name"]
        out.append(
            {
                "id": a.id,
                "analysis_id": a.analysis_id,
                "cow_id": a.cow_id,
                "cow_name": cow.name if cow else a.cow_id,
                "severity": a.severity,
                "title": care["title"] or a.title,
                "message": a.message,
                "risk_level": level,
                "confidence": a.confidence,
                "is_read": a.is_read,
                "created_at": a.created_at,
                "prediction": analysis.prediction if analysis else None,
                "yolo_class": primary_class,
                "detections": detections,
                "care_guidance": care,
                "phone": None,  # never invent
            }
        )
    return out


@router.post("/alerts/{alert_id}/read")
def mark_alert_read(alert_id: int, db: Session = Depends(get_db)):
    alert = db.get(Alert, alert_id)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert {alert_id} not found.",
        )
    alert.is_read = True
    db.commit()
    db.refresh(alert)
    return {"id": alert.id, "is_read": True}
