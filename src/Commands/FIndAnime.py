import os

import tracemoepy

from Structures.Command.BaseCommand import BaseCommand


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "whatanime",
                "category": "core",
                "description": {"content": "Identify the anime from a provided image."},
                "exp": 1,
            },
        )
        self.tracemoe = tracemoepy.tracemoe.TraceMoe()

    async def exec(self, message, context):
        reply = message.reply_to_message

        if reply and reply.media:
            path = reply.download()
            info = self.tracemoe.search(path, upload_file=True)
            data = f"Match: {info.result[0].anilist.title.romaji}\nSimilarity: {
                info.result[0].similarity * 100:.2f}%"

            video_path = f"{reply.from_user.id}.mp4"
            info.result[0].save(video_path, mute=False)

            await reply.reply_document(video_path, caption=data)
            os.remove(video_path)
