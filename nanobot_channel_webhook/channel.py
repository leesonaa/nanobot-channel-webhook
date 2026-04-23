# nanobot_channel_webhook/channel.py
import asyncio
import json
from typing import Any

from aiohttp import web
from loguru import logger

from nanobot.channels.base import BaseChannel
from nanobot.bus.events import OutboundMessage


class WebhookChannel(BaseChannel):
    name = "webhook"
    display_name = "Webhook"

    @classmethod
    def default_config(cls) -> dict[str, Any]:
        return {"enabled": False, "port": 9000, "allowFrom": []}

    def is_allowed(self, sender_id: str) -> bool:
        allow_list = self.config.get("allowFrom", [])
        if not allow_list:
            logger.warning("{}: allowFrom is empty — all access denied", self.name)
            return False
        if "*" in allow_list:
            return True
        return str(sender_id) in allow_list

    async def start(self) -> None:
        self._running = True
        port = self.config.get("port", 9000)

        app = web.Application()
        app.router.add_post("/message", self._on_request)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        logger.info("Webhook listening on :{}", port)

        while self._running:
            await asyncio.sleep(1)

        await runner.cleanup()

    async def stop(self) -> None:
        self._running = False

    async def send(self, msg: OutboundMessage) -> None:
        logger.info("[webhook] send called: {}", msg.content[:80])

    async def _on_request(self, request: web.Request) -> web.Response:
        try:
            body = await request.json()
        except Exception:
            return web.json_response({"ok": False, "error": "invalid json"}, status=400)

        title = body.get("title", "")
        text = body.get("text", "") or json.dumps(body, ensure_ascii=False, indent=2)

        if title:
            text = f"标题📪 :{title}\n内容📧 :{text}"

        # 直接转发到 QQ，不经过 AI 处理
        qq_msg = OutboundMessage(
            channel="频道",
            chat_id="你的chatid",
            content=text,
            media=[],
            metadata={},
        )
        await self.bus.publish_outbound(qq_msg)
        logger.info("[webhook] 收到消息，直接转发到 wechat: {}", text[:80])

        return web.json_response({"code": 0, "ok": True})