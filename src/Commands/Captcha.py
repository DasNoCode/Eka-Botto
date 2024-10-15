from Structures.Command.BaseCommand import BaseCommand
from pyrogram.types import ChatPermissions
from Structures.Message import Message
from captcha.image import ImageCaptcha
from Handler.EventHandler import chat_ids
import random
import string
import os
import asyncio

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "captcha",
                "category": "core",
                "description": {"content": "Prevents bots from joining"},
                "exp": 1,
            },
        )
        self.captcha_code = None
        self.captcha_message_id = None

    async def exec(self, M: Message, context):
        if not M.is_callback:
            return
        
        user_id = int(context[2].get("user_id"))
        if user_id != M.sender.user_id:
            return await self.client.answer_callback_query(
                callback_query_id=M.message_id,
                text="This Captcha isn't for you!",
                show_alert=True,
            )

        # Handling the case where the user submits a captcha code
        if context[2].get("code"):
            return await self.process_captcha_response(M, context)

        # Generate a captcha and send it to the user
        await self.send_captcha(M.chat_id, context, user_id)

    def generate_captcha(self):
        """Generates a random captcha code and its options"""
        random_text = lambda: "".join(random.choices(string.ascii_letters + string.digits, k=5))
        codes = {f"code{i}": random_text() for i in range(1, 4)}
        self.captcha_code = random.choice(list(codes.values()))
        return codes

    async def send_captcha(self, chat_id, context, user_id):
        """Creates a captcha image, sends it, and starts the timer"""

        keys = list(context[2].keys())
        codes = self.generate_captcha()
        captcha_image = ImageCaptcha(fonts=["src/CaptchaFonts/Roboto-Thin.ttf"])
        captcha_image.write(self.captcha_code, "Captcha.png")


        await self.delete_message(chat_id, chat_ids[user_id])

        # Send new captcha message
        message = await self.client.send_photo(
            chat_id,
            "Captcha.png",
            caption="__Here is your Captcha! Solve it within 1 minute.__",
            buttons=[
                {"text": code, "callback_data": f"/captcha --code={code} --user_id={user_id}"}
                for code in codes.values()
            ],
        )
        self.captcha_message_id = message.id
        asyncio.create_task(self.timer(chat_id))

        os.remove("Captcha.png")

    async def process_captcha_response(self, M: Message, context):
        """Processes the user's response to the captcha"""
        if context[2].get("code") == self.captcha_code:
            # Correct answer - grant permissions
            await self.client.restrict_chat_member(
                M.chat_id,
                M.sender.user_id,
                ChatPermissions(
                    can_send_messages=True, 
                    can_send_media_messages=True
                ),
            )
        else:
            # Incorrect answer - ban user
            await self.client.ban_chat_member(M.chat_id, M.sender.user_id)

        # Delete the captcha message after handling the response
        await self.delete_message(M.chat_id, self.captcha_message_id)

    async def timer(self, chat_id):
        """Waits for 1 minute and then deletes the captcha message if it's still there"""
        await asyncio.sleep(60)
        await self.delete_message(chat_id, self.captcha_message_id)

    async def delete_message(self, chat_id, message_id):
        """Deletes the captcha message if it exists"""
        if message_id:
            try:
                await self.client.delete_messages(chat_id=chat_id, message_ids=message_id)
            except Exception as e:
                print(f"Failed to delete captcha message: {e}")
