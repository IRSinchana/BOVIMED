"""Image validation, preprocessing, and storage helpers."""

from __future__ import annotations

import io
import uuid
from pathlib import Path

import cv2
import numpy as np
from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

from app.config import Settings, get_settings

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
}


class ImageService:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()

    async def read_and_validate(self, file: UploadFile) -> tuple[bytes, str, str]:
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No image selected. Please upload a cow/udder image.",
            )

        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Invalid file type '{ext or 'unknown'}'. "
                    "Supported formats: JPG, JPEG, PNG, WEBP."
                ),
            )

        content_type = (file.content_type or "").lower()
        if content_type and content_type not in ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported content type '{content_type}'.",
            )

        data = await file.read()
        if not data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty.",
            )

        if len(data) > self.settings.max_upload_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=(
                    f"File too large. Maximum allowed size is "
                    f"{self.settings.max_upload_size_mb} MB."
                ),
            )

        try:
            with Image.open(io.BytesIO(data)) as img:
                img.verify()
            with Image.open(io.BytesIO(data)) as img:
                img.load()
                fmt = (img.format or ext.lstrip(".")).upper()
        except (UnidentifiedImageError, OSError) as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image file. Please upload a valid cow/udder photo.",
            ) from exc

        return data, ext, fmt

    def preprocess(self, image_bytes: bytes) -> np.ndarray:
        """Decode bytes to BGR ndarray and optionally downscale large images."""
        arr = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if image is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not decode image. The file may be corrupted.",
            )

        h, w = image.shape[:2]
        max_dim = self.settings.max_image_dimension
        longest = max(h, w)
        if longest > max_dim:
            scale = max_dim / float(longest)
            image = cv2.resize(
                image,
                (int(w * scale), int(h * scale)),
                interpolation=cv2.INTER_AREA,
            )
        return image

    def save_upload(self, image_bgr: np.ndarray, ext: str = ".jpg") -> Path:
        filename = f"{uuid.uuid4().hex}{ext if ext in ALLOWED_EXTENSIONS else '.jpg'}"
        path = self.settings.uploads_dir / filename
        success = cv2.imwrite(str(path), image_bgr)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save uploaded image.",
            )
        return path

    def save_annotated(self, image_bgr: np.ndarray, stem: str | None = None) -> Path:
        name = f"{stem or uuid.uuid4().hex}_annotated.jpg"
        path = self.settings.results_dir / name
        success = cv2.imwrite(str(path), image_bgr)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save annotated image.",
            )
        return path

    @staticmethod
    def to_public_url(path: Path | str | None, kind: str) -> str | None:
        if not path:
            return None
        name = Path(path).name
        return f"/media/{kind}/{name}"


def get_image_service() -> ImageService:
    return ImageService()
