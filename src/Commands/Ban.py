from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "ban",
                "category": "core",
                "description": {"content": "Ban user from the chat"},
                "exp": 1,
            },
        )

    async def exec(self, M: Message, contex):

        if not M.isAdmin:
            return await self.client.send_message(
                M.chat_id, f"__@{M.sender.user_name} you don't have rights to do so!__."
            )

        if M.reply_to_message:
            user_name = M.sender.user_name
            user_id = M.sender.user_id
        elif M.mentioned:
            usermentioned_user = M.mentioned[0]
            user_name = usermentioned_user.user_name
            user_id = usermentioned_user.user_id

        await self.client.ban_chat_member(M.chat_id, user_id)
        await self.client.send_message(
            M.chat_id,
            f"__Successfully banned @{user_name} from {M.chat_title}__",
        )
