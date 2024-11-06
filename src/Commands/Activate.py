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
                "description": {"content": "Activate captcha and event"},
                "exp": 1,
            },
        )

    async def exec(self, M: Message, context):

        if not context[2]:
            btn = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Captcha",
                            callback_data=f"/activate --captcha={True}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Event",
                            callback_data=f"/activate --event={True}",
                        )
                    ],
                ]
            )
            return await self.client.send_message(
                M.chat_id, "What you want to activate ?", reply_markup=btn
            )
        keys = list(context[2].keys())
        if keys[0] == "captcha":
            all_captcha = self.client.db.Chat.get_all_captchas()

            if M.chat_id in all_captcha:
                return await self.client.send_message(
                    M.chat_id, f"Captcha is already activated in {M.chat_title}"
                )

            self.client.db.Chat.add_chat_id_in_captcha(M.chat_id)
            return await self.client.send_message(
                M.chat_id, f"Captcha has been activated in {M.chat_title}"
            )

        all_events = self.client.db.Chat.get_all_events()
        if M.chat_id in all_events:
            return await self.client.send_message(
                M.chat_id, f"Event is already activated in {M.chat_title}"
            )
        self.client.db.Chat.add_chat_id_in_event(M.chat_id)
        await self.client.send_message(
            M.chat_id, f"Event has been activated in {M.chat_title}"
        )
