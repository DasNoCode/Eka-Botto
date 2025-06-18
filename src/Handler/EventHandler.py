from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup

from Structures.Client import SuperClient

CHAT_IDS = {}


class EventHandler:

    def __init__(self, client: SuperClient):
        self.__client = client

    async def handler(self, message):
        self.message = message
        chat_id = message.chat.id

        if str(self.message.service).split(".")[-1] == "NEW_CHAT_MEMBERS":
            members = self.message.new_chat_members
            for member in members:
                self.member = member
            captcha = self.__client.db.Chat.get_all_captchas()
            if chat_id in captcha:
                await self.__client.restrict_chat_member(
                    self.message.chat.id,
                    self.member.id,
                    ChatPermissions(can_send_messages=False),
                )
                keybord = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Captcha",
                                callback_data=f"/captcha --type=captcha --user_id={self.member.id}",
                            )
                        ]
                    ]
                )
                print(self.member.id)
                msg = await self.__client.send_message(
                    self.message.chat.id,
                    f"__@{self.member.username} has joined the Chat !\nSolve the captcha__",
                    reply_markup=keybord,
                )

                CHAT_IDS[self.member.id] = msg.id
            else:
                await self.__client.send_message(
                    self.message.chat.id,
                    f"__@{self.member.username} has joined the Chat !__",
                )

        event = self.__client.db.Chat.get_all_events()
        if chat_id not in event:
            return
        if str(self.message.service).split(".")[-1] == "NEW_CHAT_MEMBERS":
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
            await self.__client.send_message(self.message.chat.id, f"__A new message has been pinned by @{self.message.from_user.username}./nCheck now !__",)
