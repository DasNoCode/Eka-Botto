import os
import re

from gtts import gTTS
from gtts.lang import tts_langs

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "tts",
                "category": "media",
                "AdminOnly": False,
                "OwnerOnly": False,
                "description": {"content": "Convert text to voice"},
            },
        )

    async def exec(self, M: Message, context):
        try:
            if len(context[3]) > 1:
                lang = context[3].pop(0)
                text = " ".join(context[3])
                print("msg", lang, text)
            elif M.reply_to_message:
                lang = context[3].pop(0)
                text = M.reply_to_message.text
                print("rmsg", lang, text)
            else:
                return await self.client.send_message(
                    M.chat_id, "__Reply to a message or send text__"
                )
            if lang not in tts_langs():
                return await self.client.send_message(
                    M.chat_id, "__Given language is not suported!__"
                )

            filename = re.sub(r"[^a-zA-Z0-9]", "_", text)[:15]
            filepath = f"{filename}.mp3"
            tts = gTTS(text, lang=lang)
            tts.save(filepath)
        except Exception as e:
            return await self.client.send_message(
                M.chat_id, "__Something went wrong!__"
            )

        await self.client.send_voice(
            M.chat_id, voice=filepath, caption=f"__Language : {lang}__"
        )
        os.remove(filepath)
