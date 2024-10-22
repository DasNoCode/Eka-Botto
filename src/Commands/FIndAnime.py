import os

import tracemoepy

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    media_types = {"photo": "jpg", "video": "mp4", "animation": "gif"}

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
        if M.msg_type not in self.media_types:
            return await self.client.send_message(
                M.chat_id,
                f"@{M.sender.user_name} __Replied to a Gif, Image, or Video__",
            )

        file_path = f"downloads/{M.file_id}.{self.media_types[M.msg_type]}"
        await self.client.download_media(M.file_id, file_name=file_path)

        try:
            info = self.tracemoe.search(f"src/{file_path}", upload_file=True)

            if isinstance(info.result, list) and len(info.result) > 0:
                first_result = info.result[0]
                anilist = first_result.get("anilist", {})
                if isinstance(anilist, dict):
                    title = anilist.get("title", {})
                    if isinstance(title, dict):
                        is_adult = anilist.get("isAdult", "N/A")
                        episode = first_result.get("episode", "N/A")
                        native_title = title.get("native", "N/A")
                        english_title = title.get("english", "N/A")
                        similarity = first_result.get("similarity", "N/A")
                    else:
                        native_title = english_title = "N/A"
                        similarity = episode = is_adult = "N/A"
                else:
                    native_title = english_title = "N/A"
                    similarity = episode = is_adult = "N/A"

                await self.client.send_message(
                    M.chat_id,
                    f"__Native_title__ - {native_title} \n"
                    f"__English_title__ - {english_title} \n"
                    f"__Similarity__ - {similarity * 100:.2f}% \n"
                    f"__Episode__ - {episode} \n"
                    f"__Is_adult__ - {is_adult}",
                )
            else:
                await self.client.send_message(M.chat_id, "__No results found.__")

        except Exception as e:
            self.__client.log.error(str(e))

        os.remove(f"src/{file_path}")
