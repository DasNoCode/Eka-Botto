from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "hi",
                "category": "chat",
                "AdminOnly": False,
                "OwnerOnly": True,
                "description": {"content": "Say hello to the bot"},
            },
        )

    async def exec(self, M: Message, contex):

        if self.client.owner_id != M.sender.user_id:
            return await self.client.send_message(
                M.chat_id, f"__@{M.sender.user_name} you don't have rights to do so!__."
            )

        await self.client.send_message(M.chat_id, "__Thanks for everything, See ya!__")
        await self.client.leave_chat(M.chat_id, delete=True)
