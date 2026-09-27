"""Model transparency API."""

from fastapi import APIRouter

from app.schemas import ModelInfoResponse
from app.services.model_info import get_model_info

router = APIRouter(tags=["Model"])


@router.get("/model-info", response_model=ModelInfoResponse)
def model_info():
    return ModelInfoResponse(**get_model_info())
