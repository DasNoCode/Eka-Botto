from pyigdl import IGDownloader

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "igdl",
                "category": "core",
                "description": {"content": "Download the Instagram reels and photo."},
                "exp": 1,
            },
        )

    async def exec(self, M: Message, contex):
        if not len(M.urls):
            return await self.client.send_message(
                M.chat_id, "Provide the youtube video link🔗 to download."
            )
        data = IGDownloader(M.urls[0])
        return await self.client.send_video(M.chat_id, data[0]["download_link"])
