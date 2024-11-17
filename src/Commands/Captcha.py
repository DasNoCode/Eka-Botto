import asyncio
import os
import random
import string

from captcha.image import ImageCaptcha
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup

from Handler.EventHandler import CHAT_IDS
from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "captcha",
                "category": "core",
                "AdminOnly": True,
                "OwnerOnly": False,
                "description": {"content": "Prevents bots from joining"},
            },
        )
        self.captcha_code = None
        self.captcha_message_id = None

    async def exec(self, M: Message, context):

        user_id = int(context[2].get("user_id"))
        user = await self.client.get_users(user_id)

        if not M.is_callback:
            return

        print(M.isAdmin)
        if not M.isAdmin:
            print(M.sender.user_id)
            if user_id != M.sender.user_id:
                return await self.client.answer_callback_query(
                    callback_query_id=M.message_id,
                    text="This Captcha isn't for you!",
                    show_alert=True,
                )

        if context[2].get("code"):
            if context[2].get("code") == self.captcha_code:
                await self.client.restrict_chat_member(
                    M.chat_id,
                    user_id,
                    ChatPermissions(
                        can_send_messages=True, can_send_media_messages=True
                    ),
                )
                await self.client.send_message(
                    M.chat_id, f"@{user.username}, __welcome to the chat.__"
                )
            else:
                await self.client.ban_chat_member(M.chat_id, user_id)

            await self.client.delete_messages(M.chat_id, self.captcha_message_id)
            return

        random_text = lambda: "".join(
            random.choices(string.ascii_letters + string.digits, k=5)
        )
        codes = {f"code{i}": random_text() for i in range(1, 4)}
        self.captcha_code = random.choice(list(codes.values()))

        captcha_image = ImageCaptcha(fonts=["src/CaptchaFonts/Roboto-Thin.ttf"])
        captcha_image.write(self.captcha_code, "Captcha.png")

        await self.client.delete_messages(M.chat_id, CHAT_IDS.get(user_id))

        message = await self.client.send_photo(
            M.chat_id,
            "Captcha.png",
            caption="__Here is your Captcha! Solve it within 1 minute.__",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=code,
                            callback_data=f"/captcha --code={code} --user_id={user_id}",
                        )
                    ]
                    for code in codes.values()
                ]
            ),
        )
        self.captcha_message_id = message.id

        asyncio.create_task(self.timer(M.chat_id))
        os.remove("Captcha.png")

    async def timer(self, chat_id):
        try:
            await asyncio.sleep(60)
            await self.client.delete_messages(
                chat_id=chat_id, message_ids=self.captcha_message_id
            )
        except Exception as e:
            pass
