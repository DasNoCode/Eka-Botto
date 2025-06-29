from pyrogram.types import ChatPrivileges

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "promote",
                "category": "chat",
                "xp": False,
                "AdminOnly": True,
                "OwnerOnly": False,
                "description": {"content": "Promote the user to Admin of chat"},
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

        await self.client.promote_chat_member(
            M.chat_id,
            user_id,
            ChatPrivileges(
                can_change_info=True,
                can_invite_users=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_promote_members=True,
                can_manage_video_chats=True,
                is_anonymous=False,
            ),
        )
        await self.client.send_message(
            M.chat_id,
            f"Successfully promoted @{user_name} to admin in {M.chat_title}",
        )
