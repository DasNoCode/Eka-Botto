from datetime import datetime

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "afk",
                "category": "core",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": False,
                "description": {
                    "content": "Set yourself as AFK. Mentions will auto-reply that you're unavailable and notify you when you're mentioned."
                },
            },
        )

    async def exec(self, M: Message, context):
        current_time = datetime.now().time().strftime("%H:%M:%S")
        user = self.client.db.User.get_user(M.sender.user_id)

        if user["afk"]["is_afk"]:
            return await self.client.send_message(
                M.chat_id, f"@{M.sender.user_name} you are already in afk"
            )
        self.client.db.User.set_afk(
            M.sender.user_id, True, context[1] if context[1] else None, current_time
        )
        await self.client.send_message(
            M.chat_id, f"@{M.sender.user_name} you are afk now!"
        )
