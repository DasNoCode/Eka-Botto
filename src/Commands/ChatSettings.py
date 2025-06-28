from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "set",
                "category": "core",
                "xp": False,
                "AdminOnly": True,
                "OwnerOnly": False,
                "description": {"content": "Set chat settings"},
            },
        )

    async def exec(self, M: Message, context):

        chat_data = self.client.db.Chat.get_chat_data(M.chat_id)

        if not context[2]:
            btn = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            f"Captcha {'🔐' if chat_data.get('settings').get('captchas') else '🔓'}",
                            callback_data=f"/set --type=captcha --data={True}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            f"Event {'🔔' if chat_data.get('settings').get('events') else '🔕'}",
                            callback_data=f"/set --type=events --data={True}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            f"Welcome Enabled {'ON' if chat_data.get('settings').get('welcome_enabled') else 'OFF'}",
                            callback_data=f"/set --type=welcome_enabled --data={True}",
                        )
                    ]
                ]
            )
            self.btn_msg = await self.client.send_message(
                M.chat_id, "**Chat Settings:**", reply_markup=btn
            )
            return

        if context[2].get("type") == "welcome_message":
            if not M.reply_to_message:
                await self.client.send_message(
                    M.chat_id, f"@{M.sender.user_name}, reply to the message you want to set as welcome!"
                )
            self.client.db.Chat.update_chat_datas(M.chat_id, {"settings": {"events": True}})
            self.client.db.Chat.update_chat_datas(
                M.chat_id, {"settings": {"welcome_message": M.reply_to_message.text}}
            )
            return await self.client.send_message(
                M.chat_id,
                f"**Welcome msg** set to:\n\n`{M.reply_to_message.text}`\n\nIn **{M.chat_title}**",
            )

        elif context[2].get("type") == "captcha":
            if chat_data.get("settings").get("captchas"):
                self.client.db.Chat.update_chat_datas(M.chat_id, {"settings": {"captchas": False}})
                await self.client.send_message(
                    M.chat_id, f"**Captcha** is deactivated in:\n\n**{M.chat_title}**"
                )
            else:
                self.client.db.Chat.update_chat_datas(M.chat_id, {"settings": {"captchas": True}})
                await self.client.send_message(
                    M.chat_id, f"**Captcha** is activated in:\n\n**{M.chat_title}**"
                )

        elif context[2].get("type") == "events":
            if chat_data.get("settings").get("events"):
                self.client.db.Chat.update_chat_datas(M.chat_id, {"settings": {"events": False}})
                await self.client.send_message(
                    M.chat_id,
                    f"**Event** is deactivated in (welcome msg is disabled, but you can manually turn it ON):\n\n**{M.chat_title}**",
                )
            else:
                self.client.db.Chat.update_chat_datas(M.chat_id, {"settings": {"events": True}})
                await self.client.send_message(
                    M.chat_id, f"**Event** is activated in:\n\n**{M.chat_title}**"
                )

        elif context[2].get("type") == "welcome_enabled":
            if chat_data.get("settings").get("welcome_enabled"):
                self.client.db.Chat.update_chat_datas(M.chat_id, {"settings": {"welcome_enabled": False}})
                await self.client.send_message(
                    M.chat_id, f"**Welcome msg** is deactivated in:\n\n**{M.chat_title}**"
                )
            else:
                self.client.db.Chat.update_chat_datas(M.chat_id, {"settings": {"welcome_enabled": True}})
                await self.client.send_message(
                    M.chat_id,
                    f"**Welcome msg** is activated in:\n\n**{M.chat_title}**\n\nTo set a custom welcome message, reply to any message with:\n`/set --type=welcome_message`",
                )

        return await self.client.delete_messages(chat_id=M.chat_id, message_ids=self.btn_msg.id)
