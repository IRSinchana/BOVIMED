from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class NotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cow_id: str | None = None
    type: str
    title_key: str
    message_key: str
    payload: dict[str, Any] = Field(default_factory=dict)
    severity: str
    is_read: bool
    action_url: str | None = None
    created_at: datetime


class NotificationListResponse(BaseModel):
    success: bool = True
    notifications: list[NotificationOut]
    unread_count: int


class UnreadCountResponse(BaseModel):
    success: bool = True
    unread_count: int


class NotificationPreferenceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    health_alerts: bool = True
    analysis_completed: bool = False
    veterinary_reminders: bool = True
    system_notifications: bool = True
    browser_notifications: bool = False


class NotificationPreferenceUpdate(BaseModel):
    health_alerts: bool | None = None
    analysis_completed: bool | None = None
    veterinary_reminders: bool | None = None
    system_notifications: bool | None = None
    browser_notifications: bool | None = None
