import os

from aiohttp_retry import ExponentialRetry
from shazamio import HTTPClient, Serialize, Shazam

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "shazamio",
                "category": "core",
                "description": {"content": "Identify the music playing around you"},
                "exp": 1,
            },
        )

    async def exec(self, M: Message, contex):
        shazam = Shazam(
            http_client=HTTPClient(
                retry_options=ExponentialRetry(
                    attempts=12, max_timeout=204.8, statuses={500, 502, 503, 504, 429}
                ),
            ),
        )

        def recognize(path):
            return Serialize.full_track(shazam.recognize(path))

        if M.reply_to_message:
            return await self.client.send_message(M.chat_id, "Reply to a audio !")

        if str(M.media).split(".")[-1] == "AUDIO":
            await self.client.download_media(M.audio.file_id, file_name=f"{M.id}.mp3")
            r = recognize(f"downloads/{M.id}.mp3")
            await self.client.send_photo(
                M.chat_id,
                r.track.sections[0].meta_pages[1].image,
                f"Name: {r.track.title}\nReleased: {r.track.sections[0].metadata[2].text}",
            )
            os.remove(f"downloads/{M.id}.mp3")
        elif str(M.media).split(".")[-1] == "VOICE":
            await self.client.download_media(M.voice.file_id, file_name=f"{M.id}.ogg")
            r = recognize(f"downloads/{M.id}.ogg")
            await self.client.send_photo(
                M.chat_id,
                r.track.sections[0].meta_pages[1].image,
                f"Name: {r.track.title}\nReleased: {r.track.sections[0].metadata[2].text}",
            )
            os.remove(f"downloads/{M.id}.ogg")
