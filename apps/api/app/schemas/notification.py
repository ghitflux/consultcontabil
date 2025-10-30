"""
Notification schemas for API requests and responses.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class NotificationType(str, Enum):
    """Types of notifications"""
    # Obligation related
    OBLIGATION_CREATED = "obligation_created"
    OBLIGATION_DUE_SOON = "obligation_due_soon"
    OBLIGATION_OVERDUE = "obligation_overdue"
    OBLIGATION_COMPLETED = "obligation_completed"
    OBLIGATION_CANCELED = "obligation_canceled"

    # Client related
    CLIENT_CREATED = "client_created"
    CLIENT_UPDATED = "client_updated"
    CLIENT_DOCUMENT_UPLOADED = "client_document_uploaded"

    # User related
    USER_MENTION = "user_mention"
    USER_ASSIGNED = "user_assigned"

    # System
    SYSTEM_ALERT = "system_alert"
    SYSTEM_MAINTENANCE = "system_maintenance"


class NotificationBase(BaseModel):
    """Base schema for notification"""
    type: NotificationType
    title: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1, max_length=1000)
    link: Optional[str] = Field(None, max_length=500)
    extra_data: Optional[dict] = None


class NotificationCreate(NotificationBase):
    """Schema for creating notification"""
    user_id: UUID


class NotificationBulkCreate(BaseModel):
    """Schema for creating notifications for multiple users"""
    user_ids: list[UUID]
    type: NotificationType
    title: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1, max_length=1000)
    link: Optional[str] = Field(None, max_length=500)
    extra_data: Optional[dict] = None


class NotificationUpdate(BaseModel):
    """Schema for updating notification"""
    read: Optional[bool] = None


class NotificationResponse(NotificationBase):
    """Schema for notification response"""
    id: UUID
    user_id: UUID
    read: bool
    read_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    """Schema for paginated notification list"""
    items: list[NotificationResponse]
    total: int
    unread_count: int
    page: int
    size: int
    pages: int


class NotificationMarkAllReadResponse(BaseModel):
    """Schema for mark all as read response"""
    marked_count: int
    message: str = "All notifications marked as read"


class NotificationStatistics(BaseModel):
    """Schema for notification statistics"""
    total: int
    unread: int
    by_type: dict[str, int]
    today_count: int
    this_week_count: int


# WebSocket Event Schemas
class WebSocketEventBase(BaseModel):
    """Base schema for WebSocket events"""
    type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class WebSocketNotificationEvent(WebSocketEventBase):
    """WebSocket event for new notification"""
    type: str = "notification"
    data: NotificationResponse


class WebSocketObligationUpdateEvent(WebSocketEventBase):
    """WebSocket event for obligation update"""
    type: str = "obligation_update"
    data: dict  # ObligationResponse dict


class WebSocketSystemEvent(WebSocketEventBase):
    """WebSocket event for system messages"""
    type: str = "system"
    data: dict


class WebSocketConnectedEvent(WebSocketEventBase):
    """WebSocket event for successful connection"""
    type: str = "connected"
    message: str = "WebSocket connected successfully"
    user_id: str
    role: str
