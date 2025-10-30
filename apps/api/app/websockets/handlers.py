"""
WebSocket event handlers.
"""

import logging
from typing import Optional
from uuid import UUID

from app.db.models.notification import Notification
from app.db.models.obligation import Obligation
from app.schemas.notification import NotificationResponse
from app.websockets.events import WebSocketEventBuilder
from app.websockets.manager import manager

logger = logging.getLogger(__name__)


class WebSocketHandler:
    """Handler for WebSocket events."""

    @staticmethod
    async def handle_new_notification(notification: Notification) -> bool:
        """
        Handle a new notification event.
        Sends the notification to the target user via WebSocket.

        Args:
            notification: Notification model instance

        Returns:
            bool: True if sent successfully
        """
        try:
            # Convert to response schema
            notification_response = NotificationResponse.from_orm(notification)

            # Build event
            event = WebSocketEventBuilder.notification_event(notification_response)

            # Send to user
            user_id = str(notification.user_id)
            success = await manager.send_personal_message(user_id, event)

            if success:
                logger.info(f"Notification sent to user {user_id}: {notification.type}")
            else:
                logger.debug(f"User {user_id} not connected, notification queued")

            return success

        except Exception as e:
            logger.error(f"Error handling new notification: {e}", exc_info=True)
            return False

    @staticmethod
    async def handle_obligation_created(obligation: Obligation) -> int:
        """
        Handle obligation created event.
        Notifies admin and func users.

        Args:
            obligation: Obligation model instance

        Returns:
            int: Number of users notified
        """
        try:
            from app.schemas.obligation import ObligationResponse

            # Build obligation response
            obligation_data = {
                "id": str(obligation.id),
                "client_id": str(obligation.client_id),
                "client_name": obligation.client.razao_social,
                "client_cnpj": obligation.client.cnpj,
                "obligation_type_name": obligation.obligation_type.name,
                "obligation_type_code": obligation.obligation_type.code,
                "due_date": obligation.due_date.isoformat(),
                "status": obligation.status.value,
                "priority": obligation.priority.value,
            }

            # Build event
            event = WebSocketEventBuilder.obligation_update_event(
                obligation_data,
                action="created"
            )

            # Send to admin and func users
            sent_count = await manager.broadcast_to_roles(["admin", "func"], event)

            logger.info(f"Obligation created notification sent to {sent_count} users")
            return sent_count

        except Exception as e:
            logger.error(f"Error handling obligation created: {e}", exc_info=True)
            return 0

    @staticmethod
    async def handle_obligation_updated(
        obligation: Obligation,
        action: str = "updated"
    ) -> int:
        """
        Handle obligation updated event.

        Args:
            obligation: Obligation model instance
            action: Action type (updated, completed, canceled, etc)

        Returns:
            int: Number of users notified
        """
        try:
            # Build obligation data
            obligation_data = {
                "id": str(obligation.id),
                "client_id": str(obligation.client_id),
                "client_name": obligation.client.razao_social,
                "obligation_type_name": obligation.obligation_type.name,
                "obligation_type_code": obligation.obligation_type.code,
                "status": obligation.status.value,
                "priority": obligation.priority.value,
                "due_date": obligation.due_date.isoformat(),
            }

            # Build event
            event = WebSocketEventBuilder.obligation_update_event(
                obligation_data,
                action=action
            )

            # Send to admin and func users
            sent_count = await manager.broadcast_to_roles(["admin", "func"], event)

            logger.info(f"Obligation {action} notification sent to {sent_count} users")
            return sent_count

        except Exception as e:
            logger.error(f"Error handling obligation updated: {e}", exc_info=True)
            return 0

    @staticmethod
    async def handle_system_message(
        message: str,
        severity: str = "info",
        target_roles: Optional[list[str]] = None
    ) -> int:
        """
        Handle system message broadcast.

        Args:
            message: System message
            severity: Severity level (info, warning, error)
            target_roles: Optional list of roles to target (None = all)

        Returns:
            int: Number of users notified
        """
        try:
            # Build event
            event = WebSocketEventBuilder.system_event(message, severity)

            # Send to target roles or all users
            if target_roles:
                sent_count = await manager.broadcast_to_roles(target_roles, event)
            else:
                sent_count = await manager.broadcast(event)

            logger.info(f"System message sent to {sent_count} users: {message}")
            return sent_count

        except Exception as e:
            logger.error(f"Error handling system message: {e}", exc_info=True)
            return 0

    @staticmethod
    async def handle_client_created(
        client_id: UUID,
        razao_social: str,
        cnpj: str,
        status: str
    ) -> int:
        """
        Handle client created event.

        Args:
            client_id: Client ID
            razao_social: Client name
            cnpj: Client CNPJ
            status: Client status

        Returns:
            int: Number of users notified
        """
        try:
            # Build event
            event = WebSocketEventBuilder.client_update_event(
                client_id=client_id,
                razao_social=razao_social,
                cnpj=cnpj,
                status=status,
                action="created"
            )

            # Send to admin and func users
            sent_count = await manager.broadcast_to_roles(["admin", "func"], event)

            logger.info(f"Client created notification sent to {sent_count} users")
            return sent_count

        except Exception as e:
            logger.error(f"Error handling client created: {e}", exc_info=True)
            return 0


# Global handler instance
ws_handler = WebSocketHandler()
