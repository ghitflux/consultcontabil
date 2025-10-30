"""
WebSocket Connection Manager.
Manages active WebSocket connections and message broadcasting.
"""

import logging
from typing import Dict, List, Optional

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manages WebSocket connections for real-time communication.

    Attributes:
        active_connections: Dict mapping user_id to WebSocket connection
        user_roles: Dict mapping user_id to user role
    """

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_roles: Dict[str, str] = {}

    async def connect(self, websocket: WebSocket, user_id: str, role: str) -> None:
        """
        Accept a WebSocket connection and register it.

        Args:
            websocket: WebSocket connection
            user_id: User ID (string UUID)
            role: User role (admin, func, cliente)
        """
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.user_roles[user_id] = role
        logger.info(f"WebSocket connected: user_id={user_id}, role={role}, total={len(self.active_connections)}")

    def disconnect(self, user_id: str) -> None:
        """
        Disconnect and remove a WebSocket connection.

        Args:
            user_id: User ID to disconnect
        """
        if user_id in self.active_connections:
            self.active_connections.pop(user_id, None)
            self.user_roles.pop(user_id, None)
            logger.info(f"WebSocket disconnected: user_id={user_id}, remaining={len(self.active_connections)}")

    async def send_personal_message(self, user_id: str, message: dict) -> bool:
        """
        Send a message to a specific user.

        Args:
            user_id: Target user ID
            message: Message dict to send (will be converted to JSON)

        Returns:
            bool: True if sent successfully, False if user not connected
        """
        websocket = self.active_connections.get(user_id)
        if websocket:
            try:
                await websocket.send_json(message)
                logger.debug(f"Message sent to user {user_id}: {message.get('type')}")
                return True
            except Exception as e:
                logger.error(f"Error sending message to user {user_id}: {e}")
                self.disconnect(user_id)
                return False
        else:
            logger.debug(f"User {user_id} not connected, message not sent")
            return False

    async def broadcast(
        self,
        message: dict,
        exclude: Optional[List[str]] = None
    ) -> int:
        """
        Broadcast a message to all connected users.

        Args:
            message: Message dict to broadcast
            exclude: Optional list of user IDs to exclude

        Returns:
            int: Number of users who received the message
        """
        exclude = exclude or []
        sent_count = 0

        for user_id, websocket in list(self.active_connections.items()):
            if user_id not in exclude:
                try:
                    await websocket.send_json(message)
                    sent_count += 1
                except Exception as e:
                    logger.error(f"Error broadcasting to user {user_id}: {e}")
                    self.disconnect(user_id)

        logger.debug(f"Broadcast message to {sent_count} users: {message.get('type')}")
        return sent_count

    async def broadcast_to_role(self, role: str, message: dict) -> int:
        """
        Broadcast a message to all users with a specific role.

        Args:
            role: Target role (admin, func, cliente)
            message: Message dict to broadcast

        Returns:
            int: Number of users who received the message
        """
        sent_count = 0

        for user_id, user_role in list(self.user_roles.items()):
            if user_role == role:
                success = await self.send_personal_message(user_id, message)
                if success:
                    sent_count += 1

        logger.debug(f"Broadcast message to role '{role}': {sent_count} users")
        return sent_count

    async def broadcast_to_roles(self, roles: List[str], message: dict) -> int:
        """
        Broadcast a message to all users with any of the specified roles.

        Args:
            roles: List of target roles
            message: Message dict to broadcast

        Returns:
            int: Number of users who received the message
        """
        sent_count = 0

        for user_id, user_role in list(self.user_roles.items()):
            if user_role in roles:
                success = await self.send_personal_message(user_id, message)
                if success:
                    sent_count += 1

        logger.debug(f"Broadcast message to roles {roles}: {sent_count} users")
        return sent_count

    def is_connected(self, user_id: str) -> bool:
        """
        Check if a user is connected.

        Args:
            user_id: User ID to check

        Returns:
            bool: True if connected, False otherwise
        """
        return user_id in self.active_connections

    def get_connected_users(self) -> List[str]:
        """
        Get list of all connected user IDs.

        Returns:
            List of user IDs
        """
        return list(self.active_connections.keys())

    def get_connection_count(self) -> int:
        """
        Get total number of active connections.

        Returns:
            int: Number of active connections
        """
        return len(self.active_connections)

    def get_connections_by_role(self, role: str) -> List[str]:
        """
        Get list of connected user IDs for a specific role.

        Args:
            role: Target role

        Returns:
            List of user IDs
        """
        return [
            user_id for user_id, user_role in self.user_roles.items()
            if user_role == role
        ]

    def get_connection_stats(self) -> Dict[str, int]:
        """
        Get connection statistics by role.

        Returns:
            Dict with counts per role
        """
        stats = {
            "total": len(self.active_connections),
            "admin": 0,
            "func": 0,
            "cliente": 0,
        }

        for role in self.user_roles.values():
            if role in stats:
                stats[role] += 1

        return stats


# Global instance
manager = ConnectionManager()
