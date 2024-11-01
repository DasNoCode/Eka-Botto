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
                "description": {"content": "Get the info about the server"},
                "exp": 1,
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
            f"__Status__: Working\n__Data__: {date}\n__Time__: {now}\n__Uptime__: {self.client.utils.uptime()}\n__CPU__: {cpu_usage}%\n__Memory__: {memory_usage}%",
        )
