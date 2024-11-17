from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "hi",
                "category": "core",
                "AdminOnly": False,
                "OwnerOnly": False,
                "description": {"content": "Say hello to the bot"},
                "exp": 1,
            },
        )

    async def exec(self, M: Message, contex):
        await self.client.send_message(
            M.chat_id, f"Hey, @{M.sender.user_name} how is your day today?"
        )
