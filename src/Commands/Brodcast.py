from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "brodcast",
                "category": "core",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": True,
                "description": {"content": "Say hello to the bot"},
            },
        )

    async def exec(self, M: Message, contex):
        chat_data = self.client.db.Chat.get_chat_data(M.chat_id)
        
        for chat_id in chat_data.get("chat_id"):
            await self.client.send_message(
                chat_id, f"**BRODCAST 📣**\n\n{M.reply_to_message.text}"
            )
