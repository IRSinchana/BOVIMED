from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models import Analysis
from app.schemas import AnalysisOut, AnalysisSummary
from app.services.analysis_service import AnalysisService

router = APIRouter(tags=["History"])


@router.get("/history", response_model=list[AnalysisSummary])
def list_history(
    limit: int = Query(default=50, ge=1, le=200),
    cow_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(Analysis).order_by(Analysis.timestamp.desc()).limit(limit)
    if cow_id:
        stmt = (
            select(Analysis)
            .where(Analysis.cow_id == cow_id)
            .order_by(Analysis.timestamp.desc())
            .limit(limit)
        )
    analyses = db.scalars(stmt).all()
    return [
        AnalysisSummary(
            analysis_id=a.id,
            cow_id=a.cow_id,
            prediction=a.prediction,
            confidence=a.confidence,
            risk_level=a.risk_level,
            timestamp=a.timestamp,
            model_version=a.model_version,
            demo_mode=a.demo_mode,
        )
        for a in analyses
    ]


@router.get("/history/{analysis_id}", response_model=AnalysisOut)
def get_history_item(analysis_id: int, db: Session = Depends(get_db)):
    service = AnalysisService(db)
    analysis = service.get_analysis(analysis_id)
    # Reload with detections
    analysis = db.scalar(
        select(Analysis)
        .options(selectinload(Analysis.detections))
        .where(Analysis.id == analysis_id)
    )
    return service.to_analysis_out(analysis)
