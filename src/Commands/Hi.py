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
                "xp": True,
                "AdminOnly": False,
                "OwnerOnly": False,
                "description": {"content": "Say hello to the bot"},
            },
        )

    async def exec(self, M: Message, context):
        await self.client.send_message(
            M.chat_id, f"Hey, @{M.sender.user_name} how is your day today? Use /help to user the Bot!"
        )


