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
                "category": "media",
                "AdminOnly": False,
                "OwnerOnly": False,
                "description": {"content": "Identify the music playing around you"},
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

        async def recognize(path):
            result = await shazam.recognize(path)
            return Serialize.full_track(result)

        if str(M.msg_type).split(".")[-1] == "audio":
            await self.client.download_media(M.file_id, file_name=f"{M.file_id}.mp3")
            r = await recognize(f"src/downloads/{M.file_id}.mp3")
            await self.client.send_photo(
                M.chat_id,
                r.track.sections[0].meta_pages[1].image,
                f"__Song Name__: `{r.track.title}`\n__Released__: {r.track.sections[0].metadata[2].text}",
            )
            os.remove(f"src/downloads/{M.file_id}.mp3")
        elif str(M.msg_type).split(".")[-1] == "VOICE":
            await self.client.download_media(M.voice.file_id, file_name=f"{M.id}.ogg")
            r = recognize(f"src/downloads/{M.id}.ogg")
            await self.client.send_photo(
                M.chat_id,
                r.track.sections[0].meta_pages[1].image,
                f"__Song Name__: `{r.track.title}`\n__Released__: {r.track.sections[0].metadata[2].text}",
            )
            os.remove(f"src/downloads/{M.id}.ogg")
