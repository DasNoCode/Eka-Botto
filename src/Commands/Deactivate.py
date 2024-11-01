from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "deactivate",
                "category": "core",
                "description": {"content": "Deactivate captcha and event"},
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
                            callback_data=f"/deactivate --cpatcha={False}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Event",
                            callback_data=f"/deactivate --event={False}",
                        )
                    ],
                ]
            )
            return await self.client.send_message(
                M.chat_id, "What you want to deactivate ?", reply_markup=btn
            )
        keys = list(context[2].keys())

        if keys[0] is "captcha":
            all_captcha = self.client.db.Chat.get_all_captchas()

            if M.chat_id in all_captcha:
                return

            self.client.db.Chat.add_chat_id_in_event(M.chat_id)
            await self.client.send_message(
                M.chat_id, f"Captcha has been deactivated in {M.chat_title}"
            )

        all_events = self.client.db.Chat.get_all_events()
        if M.chat_id in all_events:
            return
        self.client.db.Chat.add_chat_id_in_event(M.chat_id)
        await self.client.send_message(
            M.chat_id, f"Event has been deactivated in {M.chat_title}"
        )
