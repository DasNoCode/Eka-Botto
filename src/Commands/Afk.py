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
                "description": {
                    "content": "Set yourself to afk.When marked as AFK, any mentions will be replied to with a message to say you're not available!And that mentioned will notify you by your Assistant."
                },
                "exp": 1,
            },
        )

    async def exec(self, M: Message, context):
        current_time = datetime.now().time().strftime("%H:%M:%S")
        user = self.client.db.User.get_user(M.sender.user_id)

        if user["afk"]["is_afk"]:
            return await self.client.send_message(
                M.chat_id, f"@{M.sender.user_name} you are already in afk"
            )

        if not context[1]:
            self.client.db.User.set_afk(M.sender.user_id, True, None, current_time)
            await self.client.send_message(
                M.chat_id, f"@{M.sender.user_name} You are afk now!"
            )
        else:
            self.client.db.User.set_afk(
                M.sender.user_id, True, context[1], current_time
            )
            await self.client.send_message(
                M.chat_id, f"@{M.sender.user_name} you are afk now!"
            )
