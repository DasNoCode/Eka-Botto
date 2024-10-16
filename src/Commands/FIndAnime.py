import os

import tracemoepy

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

# tracemoe = tracemoepy.tracemoe.TraceMoe()
#
# print(
#    tracemoe.search(
#        "/home/das/Desktop/Robotto-Bot12/Images/download.jpeg", upload_file=True
#    )
# )


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

    async def exec(self, M: Message, contex):

        if M.msg_type not in ["animation", "photo", "video"]:
            return
        print(M.file_id)
        try:
            await self.client.download_media(
                M.file_id, file_name=f"downloads/{M.file_id}.jpg"
            )
        except Exception as e:
            print(e)
        await self.client.send_message(M.chat_id, M.msg_type)

        # if M.reply_to_message:


#
#    path = reply.download()
#    info = self.tracemoe.search(path, upload_file=True)
#    data = f"Match: {info.result[0].anilist.title.romaji}\nSimilarity: {
#       info.result[0].similarity * 100:.2f}%"
#    video_path = f"{reply.from_user.id}.mp4"
#    info.result[0].save(video_path, mute=False)
#    await reply.reply_document(video_path, caption=data)
#    os.remove(video_path)
