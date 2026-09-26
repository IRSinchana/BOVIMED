from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models import Analysis, Cow
from app.schemas import AnalysisOut, CowCreate, CowOut
from app.services.analysis_service import AnalysisService

router = APIRouter(tags=["Cows"])


def _cow_to_out(db: Session, cow: Cow) -> CowOut:
    latest = db.scalar(
        select(Analysis)
        .where(Analysis.cow_id == cow.cow_id)
        .order_by(Analysis.timestamp.desc())
        .limit(1)
    )
    count = db.scalar(
        select(func.count()).select_from(Analysis).where(Analysis.cow_id == cow.cow_id)
    ) or 0
    status_label = latest.risk_level if latest else None
    return CowOut(
        id=cow.id,
        cow_id=cow.cow_id,
        name=cow.name,
        breed=cow.breed,
        age=cow.age,
        farm_location=cow.farm_location,
        notes=cow.notes,
        created_at=cow.created_at,
        updated_at=cow.updated_at,
        current_status=status_label,
        last_analysis_at=latest.timestamp if latest else None,
        analysis_count=count,
    )


@router.post("/cows", response_model=CowOut, status_code=status.HTTP_201_CREATED)
def create_cow(payload: CowCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(Cow).where(Cow.cow_id == payload.cow_id.strip()))
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cow '{payload.cow_id}' already exists.",
        )
    cow = Cow(
        cow_id=payload.cow_id.strip(),
        name=payload.name,
        breed=payload.breed,
        age=payload.age,
        farm_location=payload.farm_location,
        notes=payload.notes,
    )
    try:
        db.add(cow)
        db.commit()
        db.refresh(cow)
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database failure while creating cow.",
        ) from exc
    return _cow_to_out(db, cow)


@router.get("/cows", response_model=list[CowOut])
def list_cows(db: Session = Depends(get_db)):
    cows = db.scalars(select(Cow).order_by(Cow.cow_id.asc())).all()
    return [_cow_to_out(db, c) for c in cows]


@router.get("/cows/{cow_id}", response_model=CowOut)
def get_cow(cow_id: str, db: Session = Depends(get_db)):
    cow = db.scalar(select(Cow).where(Cow.cow_id == cow_id))
    if not cow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cow '{cow_id}' not found.",
        )
    return _cow_to_out(db, cow)


@router.get("/cows/{cow_id}/history", response_model=list[AnalysisOut])
def get_cow_history(cow_id: str, db: Session = Depends(get_db)):
    cow = db.scalar(select(Cow).where(Cow.cow_id == cow_id))
    if not cow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cow '{cow_id}' not found.",
        )
    analyses = db.scalars(
        select(Analysis)
        .options(selectinload(Analysis.detections))
        .where(Analysis.cow_id == cow_id)
        .order_by(Analysis.timestamp.desc())
    ).all()
    service = AnalysisService(db)
    return [service.to_analysis_out(a) for a in analyses]
