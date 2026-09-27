"""In-app notification center and preferences."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.notification import (
    NotificationListResponse,
    NotificationOut,
    NotificationPreferenceOut,
    NotificationPreferenceUpdate,
    UnreadCountResponse,
)
from app.services.auth_service import get_current_user
from app.services.notification_service import (
    get_or_create_preferences,
    list_notifications,
    mark_all_read,
    mark_read,
    unread_count,
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=NotificationListResponse)
def get_notifications(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = list_notifications(db, current_user.id, limit=limit)
    count = unread_count(db, current_user.id)
    return NotificationListResponse(
        notifications=[NotificationOut.model_validate(n) for n in items],
        unread_count=count,
    )


@router.get("/unread-count", response_model=UnreadCountResponse)
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return UnreadCountResponse(unread_count=unread_count(db, current_user.id))


@router.patch("/{notification_id}/read", response_model=NotificationOut)
def patch_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notif = mark_read(db, current_user.id, notification_id)
    if not notif:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found.")
    return NotificationOut.model_validate(notif)


@router.patch("/read-all")
def patch_read_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated = mark_all_read(db, current_user.id)
    return {"success": True, "updated": updated}


@router.get("/preferences", response_model=NotificationPreferenceOut)
def get_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prefs = get_or_create_preferences(db, current_user.id)
    return NotificationPreferenceOut.model_validate(prefs)


@router.put("/preferences", response_model=NotificationPreferenceOut)
def update_preferences(
    payload: NotificationPreferenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prefs = get_or_create_preferences(db, current_user.id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(prefs, key, value)
    db.add(prefs)
    db.commit()
    db.refresh(prefs)
    return NotificationPreferenceOut.model_validate(prefs)
