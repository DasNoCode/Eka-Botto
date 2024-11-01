from pyrogram.types import ChatPermissions

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "lockchat",
                "category": "chat",
                "description": {"content": "Lock the chat"},
                "exp": 1,
            },
        )

    async def exec(self, M: Message, contex):

        # if not M.isAdmin:
        #     return await self.client.send_message(
        #         M.chat_id, f"__@{M.sender.user_name} you don't have rights to do so!__."
        #     )
        if (
            self.M.chat_info.permissions.get("can_send_messages")
            and self.M.chat_info.permissions.get("can_send_media_messages")
            and self.M.chat_info.permissions.get("can_send_other_messages")
        ):
            await self.client.set_chat_permissions(
                chat_id=M.chat_id,
                permissions=ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_polls=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False,
                ),
            )
            return await self.client.send_message(
                M.chat_id, f"__{M.chat_title} have been muted by @{M.sender.user_name}."
            )
        await self.client.set_chat_permissions(
            chat_id=M.chat_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
            ),
        )
        return await self.client.send_message(
            M.chat_id, f"__{M.chat_title} have been unmuted by @{M.sender.user_name}."
        )
