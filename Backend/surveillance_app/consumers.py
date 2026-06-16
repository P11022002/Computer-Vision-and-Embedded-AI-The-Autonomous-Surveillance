from __future__ import annotations

import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


class ControlConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        await self.accept()
        await self.send(json.dumps({"type": "connection", "message": "control socket connected"}))
        logger.info("WebSocket control client connected")

    async def disconnect(self, code: int) -> None:
        logger.info("WebSocket control client disconnected: %s", code)

    async def receive(self, text_data: str = "", bytes_data: bytes | None = None) -> None:
        try:
            payload = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(json.dumps({"error": "invalid json"}))
            return

        action = payload.get("action")
        if action not in {"forward", "backward", "left", "right", "stop", "autonomous"}:
            await self.send(json.dumps({"error": "invalid action"}))
            return

        logger.info("WebSocket received action: %s", action)
        await self.send(json.dumps({"status": "received", "action": action}))
