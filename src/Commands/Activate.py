from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "activate",
                "category": "core",
                "xp": False,
                "AdminOnly": True,
                "OwnerOnly": False,
                "description": {"content": "Activate captcha and event"},
            },
        )

    async def exec(self, M: Message, context):

        if not context[2]:
            btn = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Captcha",
                            callback_data=f"/activate --type=captcha --data={True}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Event",
                            callback_data=f"/activate --type=event --data={True}",
                        )
                    ],
                ]
            )
            return await self.client.send_message(
                M.chat_id, "What you want to activate ?", reply_markup=btn
            )
        
        chat_data = self.client.db.Chat.get_chat_data(M.chat_id)

        if context[2].get("type") == "captcha":
            
            if chat_data.get("settings").get("captchas"):
                return await self.client.send_message(
                    M.chat_id, f"**Captcha** is already activated in:\n\n{M.chat_title}"
                )

            self.client.db.Chat.update_chat_datas(M.chat_id,{"settings": {"captchas": True}})
            return await self.client.send_message(
                M.chat_id, f"**Captcha** has been activated in:\n\n{M.chat_title}"
            )

        if chat_data.get("settings").get("events"):
            return await self.client.send_message(
                M.chat_id, f"**Event** is already activated in:\n\n{M.chat_title}"
            )
        self.client.db.Chat.update_chat_datas(M.chat_id,{"settings": {"events": True}})
        await self.client.send_message(
            M.chat_id, f"**Event** has been activated in:\n\n{M.chat_title}"
        )



