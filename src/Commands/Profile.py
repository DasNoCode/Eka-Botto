import os

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "profile",
                "category": "core",
                "description": {"content": "Send the profile picture of the user."},
                "exp": 1,
            },
        )

    async def exec(self, M: Message, contex):
        try:
            if M.reply_to_message:
                print(M.mentioned[0])
                await self.client.download_media(
                    M.mentioned[0].user_profile_id,
                    file_name=f"downloads/{M.mentioned[0].user_profile_id}.jpg",
                )
                await self.client.send_photo(
                    M.chat_id,
                    photo=f"src/downloads/{M.mentioned[0].user_profile_id}.jpg",
                    caption=f"__Username__: @{M.mentioned[0].user_name}\n__UserID__: {M.mentioned[0].user_id}",
                )
                return os.remove(f"src/downloads/{M.mentioned[0].user_profile_id}.jpg")

            await self.client.download_media(
                M.sender.user_profile_id,
                file_name=f"downloads/{M.sender.user_profile_id}.jpg",
            )
            await self.client.send_photo(
                M.chat_id,
                photo=f"src/downloads/{M.sender.user_profile_id}.jpg",
                caption=f"__Username__: @{M.sender.user_name}\n__UserID__: {M.sender.user_id}",
            )
            os.remove(f"src/downloads/{M.sender.user_profile_id}.jpg")
        except Exception as e:
            self.client.log.error(str(e))
