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
                "xp": False,
                "AdminOnly": True,
                "OwnerOnly": False,
                "description": {"content": "Lock the chat"},
            },
        )

    async def exec(self, M: Message, contex):

        chat_id = M.chat_id

        if M.chat_info.permissions.can_send_messages:
            self.client.db.Chat.add_Chat_permissions(chat_id, M.chat_info.permissions)
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
                M.chat_id,
                f"__@{M.chat_title} have been muted by @{M.sender.user_name}.",
            )
        chatpermissions = self.client.db.Chat.get_all_chatpermissions()
        await self.client.set_chat_permissions(
            chat_id,
            permissions=ChatPermissions(
                can_send_messages=chatpermissions[f"{chat_id}"]["can_send_messages"],
                can_send_media_messages=chatpermissions[f"{chat_id}"][
                    "can_send_media_messages"
                ],
                can_send_polls=chatpermissions[f"{chat_id}"]["can_send_polls"],
                can_send_other_messages=chatpermissions[f"{chat_id}"][
                    "can_send_other_messages"
                ],
                can_add_web_page_previews=chatpermissions[f"{chat_id}"][
                    "can_add_web_page_previews"
                ],
            ),
        )
        return await self.client.send_message(
            chat_id, f"__@{M.chat_title} have been unmuted by @{M.sender.user_name}."
        )
