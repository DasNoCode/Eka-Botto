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
                "description": {"content": "Say hello to the bot"},
                "exp": 1,
            },
        )

    async def exec(self, M: Message, contex):

        # if not M.isAdmin:
        #     return await self.client.send_message(
        #         M.chat_id, f"__@{M.sender.user_name} you don't have rights to do so!__."
        #     )

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
