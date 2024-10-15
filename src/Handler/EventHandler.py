from pyrogram.types import ChatPermissions

from Structures.Client import SuperClient

CHAT_IDS = {}


class EventHandler:

    def __init__(self, client: SuperClient):
        self.__client = client

    async def handler(self, message):
        self.message = message

        event = True
        if event != True:  # add mongo
            return

        if str(self.message.service).split(".")[-1] == "NEW_CHAT_MEMBERS":
            members = self.message.new_chat_members
            for member in members:
                self.member = member
            captcha = True
            if captcha:  # add mongo
                await self.__client.restrict_chat_member(
                    self.message.chat.id,
                    self.member.id,
                    ChatPermissions(can_send_messages=False),
                )
                keybord = [
                    {
                        "text": "Captcha",
                        "callback_data": f"/captcha --type=captcha --user_id={self.member.id}",
                    }
                ]
                msg = await self.__client.send_message(
                    self.message.chat.id,
                    f"__@{self.member.username} has joined the Chat !\nSolve the captcha__",
                    buttons=keybord,
                )

                CHAT_IDS[self.member.id] = msg.id
            else:
                await self.__client.send_message(
                    self.message.chat.id,
                    f"__@{self.member.username} has joined the Chat !__",
                )
        elif str(self.message.service).split(".")[-1] == "LEFT_CHAT_MEMBERS":
            await self.__client.send_message(
                self.message.chat.id,
                f"__@{self.message.left_chat_member.username} has left the Chat.__",
            )
        elif str(self.message.service).split(".")[-1] == "PINNED_MESSAGE":
            await self.__client.send_message(
                self.message.chat.id,
                f"__A new message has been pinned by @{
                    self.message.from_user.username}.\nCheck now !__",
            )
