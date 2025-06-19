from pyrogram.types import ChatPermissions

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "mute",
                "category": "chat",
                "xp": False,
                "AdminOnly": True,
                "OwnerOnly": False,
                "description": {"content": "Say hello to the bot"},
            },
        )

    async def exec(self, M: Message, contex):

        if M.reply_to_message:
            user_name = M.sender.user_name
            user_id = M.sender.user_id
        elif M.mentioned:
            usermentioned_user = M.mentioned[0]
            user_name = usermentioned_user.user_name
            user_id = usermentioned_user.user_id

        await self.client.restrict_chat_member(M.chat_id, user_id, ChatPermissions())
        await self.client.send_message(
            M.chat_id,
            f"__Successfully muted @{user_name} from {M.chat_title}__",
        )
