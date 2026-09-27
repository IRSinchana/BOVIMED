from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas import AnalysisOut
from app.services.analysis_service import AnalysisService
from app.services.auth_service import get_optional_current_user

router = APIRouter(tags=["Analysis"])


@router.post("/analyze", response_model=AnalysisOut)
async def analyze_image(
    image: UploadFile = File(..., description="Cow/udder image (JPG, PNG, WEBP)"),
    cow_id: str | None = Form(default=None, description="Optional cow ID, e.g. COW-001"),
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    """
    Upload an image for AI-assisted mastitis screening.

    Pipeline: validate → preprocess → YOLO11 (or DEMO) → risk → recommendations → save.
    """
    service = AnalysisService(db)
    return await service.analyze(
        image,
        cow_id=cow_id,
        user_id=current_user.id if current_user else None,
    )
