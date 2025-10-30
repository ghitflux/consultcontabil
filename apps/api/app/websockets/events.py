"""
WebSocket event types and builders.
"""

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from app.schemas.notification import (
    NotificationResponse,
    WebSocketConnectedEvent,
    WebSocketNotificationEvent,
    WebSocketObligationUpdateEvent,
    WebSocketSystemEvent,
)


class WebSocketEventBuilder:
    """Helper class to build WebSocket events."""

    @staticmethod
    def connected_event(user_id: str, role: str) -> Dict[str, Any]:
        """
        Build a connected event.

        Args:
            user_id: User ID
            role: User role

        Returns:
            Dict representing the event
        """
        event = WebSocketConnectedEvent(
            user_id=user_id,
            role=role,
            timestamp=datetime.utcnow().isoformat()
        )
        return event.dict()

    @staticmethod
    def notification_event(notification: NotificationResponse) -> Dict[str, Any]:
        """
        Build a notification event.

        Args:
            notification: Notification response schema

        Returns:
            Dict representing the event
        """
        event = WebSocketNotificationEvent(
            data=notification,
            timestamp=datetime.utcnow().isoformat()
        )
        return event.dict()

    @staticmethod
    def obligation_update_event(
        obligation_data: Dict[str, Any],
        action: str = "updated"
    ) -> Dict[str, Any]:
        """
        Build an obligation update event.

        Args:
            obligation_data: Obligation data dict
            action: Action type (created, updated, completed, canceled)

        Returns:
            Dict representing the event
        """
        data = {
            **obligation_data,
            "action": action
        }
        event = WebSocketObligationUpdateEvent(
            data=data,
            timestamp=datetime.utcnow().isoformat()
        )
        return event.dict()

    @staticmethod
    def system_event(
        message: str,
        severity: str = "info",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Build a system event.

        Args:
            message: System message
            severity: Severity level (info, warning, error)
            **kwargs: Additional data

        Returns:
            Dict representing the event
        """
        data = {
            "message": message,
            "severity": severity,
            **kwargs
        }
        event = WebSocketSystemEvent(
            data=data,
            timestamp=datetime.utcnow().isoformat()
        )
        return event.dict()

    @staticmethod
    def client_update_event(
        client_id: UUID,
        razao_social: str,
        cnpj: str,
        status: str,
        action: str = "updated"
    ) -> Dict[str, Any]:
        """
        Build a client update event.

        Args:
            client_id: Client ID
            razao_social: Client name
            cnpj: Client CNPJ
            status: Client status
            action: Action type (created, updated, deleted)

        Returns:
            Dict representing the event
        """
        return {
            "type": "client_update",
            "data": {
                "id": str(client_id),
                "razao_social": razao_social,
                "cnpj": cnpj,
                "status": status,
                "action": action
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    @staticmethod
    def user_mention_event(
        mentioned_by: str,
        mentioned_by_id: UUID,
        context: str,
        context_id: UUID,
        message: str,
        link: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Build a user mention event.

        Args:
            mentioned_by: Name of user who mentioned
            mentioned_by_id: ID of user who mentioned
            context: Context type (obligation, comment, etc)
            context_id: Context ID
            message: Mention message
            link: Optional link to context

        Returns:
            Dict representing the event
        """
        return {
            "type": "user_mention",
            "data": {
                "mentioned_by": mentioned_by,
                "mentioned_by_id": str(mentioned_by_id),
                "context": context,
                "context_id": str(context_id),
                "message": message,
                "link": link
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    @staticmethod
    def ping_event() -> Dict[str, str]:
        """
        Build a ping event.

        Returns:
            Dict with pong message
        """
        return {
            "type": "pong",
            "timestamp": datetime.utcnow().isoformat()
        }


# Convenience function
def build_event(event_type: str, data: Any) -> Dict[str, Any]:
    """
    Build a generic event.

    Args:
        event_type: Type of event
        data: Event data

    Returns:
        Dict representing the event
    """
    return {
        "type": event_type,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }
