import os
import re

from gtts import gTTS

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


# not ready
class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "voice",
                "category": "media",
                "description": {"content": "Convert text to voice"},
                "exp": 1,
            },
        )
        self.lang = "ja"

    async def exec(self, M: Message, context):

        print(context)
        text = M.message.split()
        if len(context) > 2 and context[2].get("lang"):
            self.lang = context[2].get("lang")
            print(self.lang)

        if len(text) > 1:
            msg = " ".join(text[1:])
        elif M.reply_to_message and len(text) == 1:
            msg = M.reply_to_message.text
        else:
            return await self.client.send_message(
                M.chat_id, "__Reply to a message or send text__"
            )

        filename = re.sub(r"[^a-zA-Z0-9]", "_", msg)[:15]
        filepath = f"{filename}.mp3"

        tts = gTTS(msg, lang=self.lang)
        tts.save(filepath)

        await self.client.send_voice(
            M.chat_id, voice=filepath, caption=f"__Language : {self.lang}__"
        )
        os.remove(filepath)
