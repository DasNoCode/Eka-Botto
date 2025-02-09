import re

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Helpers.Ytdl import YouTubeDownloader
from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "ytdl",
                "category": "media",
                "AdminOnly": False,
                "OwnerOnly": False,
                "description": {
                    "content": "Download Youtube videos and music",
                    "usage": "ytdl [url]",
                },
            },
        )

    async def exec(self, M: Message, context):
        keys = list(context[2].keys())
        if len(keys) > 0:
            if keys[0] == "video":
                try:
                    title, path, length = YouTubeDownloader.video_dl(
                        url=context[2][keys[0]]
                    )
                    return await self.client.send_video(
                        M.chat_id,
                        path,
                        caption=f"Title: {title}\nDuration: {length // 60, length % 60}",
                    )
                    YouTubeDownloader.delete()
                except Exception as e:
                    self.__client.log.error(e)
                    return await self.client.send_message(
                        M.chat_id, "Something went wrong !"
                    )
            if keys[0] == "audio":
                try:
                    title, path, length = YouTubeDownloader.audio_dl(
                        url=context[2][keys[0]]
                    )
                    return await self.client.send_audio(
                        M.chat_id,
                        path,
                        caption=f"Title: {title}\nDuration: {length // 60}:{length % 60}",
                    )
                    YouTubeDownloader.delete()
                except Exception as e:
                    self.__client.log.error(e)
                    return await self.client.send_message(
                        M.chat_id, "Something went wrong !"
                    )

        if not M.urls:
            return await self.client.send_message(
                M.chat_id, "Provide the youtube video link🔗 to download."
            )

        url = M.urls[0]
        match = re.search(r"(?:be\/|v=)([^&\/?]+)\?si=[\w]+", url)
        media_id = match.group(1) if match else None
        btn = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "YouTube video 📼", callback_data=f"/ytdl --video={media_id}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "YouTube Music 🎶", callback_data=f"/ytdl --audio={media_id}"
                    )
                ],
            ]
        )
        await self.client.send_message(
            M.chat_id, "What you want to download ?", reply_markup=btn
        )
