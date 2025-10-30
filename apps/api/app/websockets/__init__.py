"""
WebSocket module for real-time communication.
"""

from app.websockets.events import WebSocketEventBuilder, build_event
from app.websockets.handlers import WebSocketHandler, ws_handler
from app.websockets.manager import ConnectionManager, manager

__all__ = [
    "ConnectionManager",
    "manager",
    "WebSocketHandler",
    "ws_handler",
    "WebSocketEventBuilder",
    "build_event",
]
