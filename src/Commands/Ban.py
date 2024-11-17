from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "ban",
                "category": "chat",
                "AdminOnly": False,
                "OwnerOnly": True,
                "description": {"content": "Ban user from using the bot"},
            },
        )

    async def exec(self, M: Message, context):

        if M.reply_to_message:
            user_name = M.sender.user_name
            user_id = M.sender.user_id
        elif M.mentioned:
            usermentioned_user = M.mentioned[0]
            user_name = usermentioned_user.user_name
            user_id = usermentioned_user.user_id

        self.client.db.User.update_ban(user_id, True, context[1], None)
        await self.client.send_message(
            M.chat_id,
            f"__Successfully banned @{user_name} from using {M.bot_username}__",
        )
