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
                "AdminOnly": False,
                "OwnerOnly": True,
                "description": {"content": "Say hello to the bot"},
            },
        )

    async def exec(self, M: Message, contex):
        chat_ids = self.client.db.Botdb.get_all_chat_id()
        for chat_id in chat_ids:
            await self.client.send_message(
                chat_id, f"__**BRODCAST**__\n{M.reply_to_message.text}"
            )
