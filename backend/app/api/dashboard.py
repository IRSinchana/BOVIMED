from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models import Alert, Analysis, Cow
from app.schemas import AnalysisSummary, DashboardStats
from app.services.risk_engine import RiskEngine

router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard(db: Session = Depends(get_db)):
    settings = get_settings()
    now = datetime.now(timezone.utc)

    total_cows = db.scalar(select(func.count()).select_from(Cow)) or 0
    total_analyses = db.scalar(select(func.count()).select_from(Analysis)) or 0
    unread_alerts = (
        db.scalar(select(func.count()).select_from(Alert).where(Alert.is_read.is_(False)))
        or 0
    )

    analyses_this_month = (
        db.scalar(
            select(func.count())
            .select_from(Analysis)
            .where(
                extract("year", Analysis.timestamp) == now.year,
                extract("month", Analysis.timestamp) == now.month,
            )
        )
        or 0
    )

    # Latest analysis per cow for healthy / at-risk counts
    cows = db.scalars(select(Cow)).all()
    healthy = 0
    monitoring = 0
    at_risk = 0
    for cow in cows:
        latest = db.scalar(
            select(Analysis)
            .where(Analysis.cow_id == cow.cow_id)
            .order_by(Analysis.timestamp.desc())
            .limit(1)
        )
        if not latest:
            continue
        level = latest.risk_level
        if level in ("Low", "Healthy", RiskEngine.LOW, RiskEngine.HEALTHY):
            healthy += 1
        elif level in ("Mild", RiskEngine.MILD):
            monitoring += 1
        else:
            at_risk += 1

    risk_distribution = {
        "Low": 0,
        "Mild": 0,
        "Moderate": 0,
        "High": 0,
        "Critical": 0,
        "Healthy": 0,
        "Severe": 0,
    }
    rows = db.execute(
        select(Analysis.risk_level, func.count()).group_by(Analysis.risk_level)
    ).all()
    for level, count in rows:
        if level in risk_distribution:
            risk_distribution[level] = count

    # Last 6 months analysis counts
    monthly: list[dict] = []
    for offset in range(5, -1, -1):
        month = now.month - offset
        year = now.year
        while month <= 0:
            month += 12
            year -= 1
        count = (
            db.scalar(
                select(func.count())
                .select_from(Analysis)
                .where(
                    extract("year", Analysis.timestamp) == year,
                    extract("month", Analysis.timestamp) == month,
                )
            )
            or 0
        )
        monthly.append(
            {
                "year": year,
                "month": month,
                "label": datetime(year, month, 1).strftime("%b %Y"),
                "count": count,
            }
        )

    recent = db.scalars(
        select(Analysis).order_by(Analysis.timestamp.desc()).limit(10)
    ).all()
    recent_analyses = [
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
        for a in recent
    ]

    return DashboardStats(
        total_cows=total_cows,
        healthy=healthy,
        monitoring=monitoring,
        at_risk=at_risk,
        analyses_this_month=analyses_this_month,
        total_analyses=total_analyses,
        unread_alerts=unread_alerts,
        risk_distribution=risk_distribution,
        monthly_analyses=monthly,
        recent_analyses=recent_analyses,
        demo_mode=settings.should_use_demo_mode(),
    )
