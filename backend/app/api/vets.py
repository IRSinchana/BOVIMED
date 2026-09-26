"""Veterinarian finder API — never invents contacts."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.chat import VeterinarianSearch
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.vet_service import get_veterinarian_service

router = APIRouter(prefix="/veterinarians", tags=["Veterinarians"])


class VetSearchRequest(BaseModel):
    state: str | None = None
    district: str | None = None
    city: str | None = None
    pincode: str | None = None
    latitude: float | None = None
    longitude: float | None = None


@router.post("/search")
def search_veterinarians(
    payload: VetSearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = get_veterinarian_service()
    result = service.search(
        state=payload.state,
        district=payload.district,
        city=payload.city,
        pincode=payload.pincode,
        latitude=payload.latitude,
        longitude=payload.longitude,
    )
    try:
        db.add(
            VeterinarianSearch(
                user_id=current_user.id,
                state=payload.state,
                district=payload.district,
                city=payload.city,
                pincode=payload.pincode,
                result_status=result.get("status"),
            )
        )
        db.commit()
    except Exception:  # noqa: BLE001
        db.rollback()
    return result
