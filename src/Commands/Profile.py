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
                "AdminOnly": False,
                "OwnerOnly": False,
                "description": {"content": "Send the profile picture of the user."},
                "exp": 1,
            },
        )

    async def exec(self, M: Message, contex):
        print(M.reply_to_message)

        if M.reply_to_message:
            await self.client.download_media(
                M.reply_to_message.replied_user.user_profile_id,
                file_name=f"downloads/{M.reply_to_message.replied_user.user_profile_id}.jpg",
            )
            await self.client.send_photo(
                M.chat_id,
                photo=f"src/downloads/{M.reply_to_message.replied_user.user_profile_id}.jpg",
                caption=f"__Username__: @{M.reply_to_message.replied_user.user_name}\n__UserID__: {M.reply_to_message.replied_user.user_id}",
            )
            return os.remove(
                f"src/downloads/{M.reply_to_message.replied_user.user_profile_id}.jpg"
            )
        elif M.mentioned:
            mentioned_user = M.mentioned[0]
            await self.client.download_media(
                mentioned_user.user_profile_id,
                file_name=f"downloads/{mentioned_user.user_profile_id}.jpg",
            )
            print("user profile ")
            await self.client.send_photo(
                M.chat_id,
                photo=f"src/downloads/{mentioned_user.user_profile_id}.jpg",
                caption=f"__Username__: @{mentioned_user.user_name}\n__UserID__: {mentioned_user.user_id}",
            )
            return os.remove(f"src/downloads/{mentioned_user.user_profile_id}.jpg")
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
