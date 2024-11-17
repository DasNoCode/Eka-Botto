import requests

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "weather",
                "category": "core",
                "AdminOnly": False,
                "OwnerOnly": False,
                "description": {"content": "Get the current weather for a location"},
                "exp": 1,
            },
        )

    async def exec(self, M: Message, contex):

        if len(M.message) < 2:
            await self.client.send_message(
                M.chat_id, f"Send **/weather location** to get weather info ℹ️."
            )
            return
        try:
            location = " ".join(M.message[1:])
            response = requests.get(f"https://wttr.in/{location}?mnTC0&lang=en")
            await self.client.send_message(M.chat_id, response.text)
        except Exception as e:
            self.__client.log.error(str(e))
            await self.client.send_message(M.chat_id, f"__Error:__ {e}")
