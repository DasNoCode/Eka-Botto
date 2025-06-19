from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "chatid",
                "category": "core",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": False,
                "description": {"content": "Give id of the chat"},
                "exp": 1,
            },
        )

    async def exec(self, M: Message, contex):
        await self.client.send_message(M.chat_id, f"__chat-id__: `{M.chat_id}`")
