from Structures.Command.BaseCommand import BaseCommand
from pyrogram.types import ChatPermissions
from Structures.Message import Message
from captcha.image import ImageCaptcha
import random
import string
import os


class Command(BaseCommand):

    captcha_code = ""

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "captcha",
                "category": "core",
                "description": {"content": "Privents from bots"},
                "exp": 1,
            },
        )

    async def exec(self, M: Message, contex):

        keys = list(contex[2].keys())

        if not M.is_callback:
            return

        if keys[0] == "code":
            if contex[2][keys[0]] == self.captcha_code:
                return await self.client.restrict_chat_member(
                    M.chat_id,
                    M.sender.user_id,
                    ChatPermissions(
                        can_send_messages=True, can_send_media_messages=True
                    ),
                )
            else:
                return await self.__client.ban_chat_member(M.chat_id, M.sender.user_id)

        if int(contex[2][keys[1]]) != M.sender.user_id:
            return await self.client.answer_callback_query(
                callback_query_id=M.message_id,
                text="This Captcha isn't for you !",
                show_alert=True,
            )

        random_text = lambda: "".join(
            random.choices(string.ascii_letters + string.digits, k=5)
        )

        codes = {f"code{i}": random_text() for i in range(1, 4)}
        code1, code2, code3 = codes["code1"], codes["code2"], codes["code3"]
        self.captcha_code = random.choice([code1, code2, code3])
        captcha_image = ImageCaptcha(fonts=["src/CaptchaFonts/Roboto-Thin.ttf"])
        captcha_image.write(self.captcha_code, "Captcha.png")
        keybord = [
            {"text": code1, "callback_data": f"/captcha --code={code1}"},
            {"text": code2, "callback_data": f"/captcha --code={code2}"},
            {"text": code3, "callback_data": f"/captcha --code={code3}"},
        ]
        await self.client.send_photo(
            M.chat_id,
            "Captcha.png",
            caption=f"__Here is your Captcha !\nkindly Solve it under 1 min.__",
            buttons=keybord,
        )
        os.remove("Captcha.png")
