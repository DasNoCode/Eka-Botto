from datetime import datetime

import psutil

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "stats",
                "category": "utility",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": True,
                "description": {"content": "Get the info about the server"},
            },
        )

    async def exec(self, M: Message, contex):
        cpu_usage = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
        now = datetime.now().time().strftime("%H:%M:%S")
        date = datetime.now().strftime("%Y-%m-%d")
        await self.client.send_message(
            M.chat_id,
            f"💻  **Status**\n\n**Data:** {date}\n\n**Time:** {now}\n\n**Uptime:** {self.client.utils.uptime()}\n\n**CPU:** {cpu_usage}%\n\n**Memory:** {memory_usage}%",
        )
