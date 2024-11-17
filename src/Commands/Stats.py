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
            f"• **Status**: __Working__\n• **Data**: __{date}__\n• **Time**: __{now}__\n• **Uptime**: __{self.client.utils.uptime()}__\n• **CPU**: __{cpu_usage}%__\n• **Memory**: __{memory_usage}%__",
        )
