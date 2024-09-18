from Structures.Client import SuperClient


class EventHandler:
    def __init__(self, client: SuperClient):
        self.__client = client

    async def handler(self, message):
        self.message = message
        self.user_id = self.message.from_user.id
        self.username = self.message.from_user.username
        event = True
        if event:  # add mongo
            if str(self.message.service).split(".")[-1] == "NEW_CHAT_MEMBERS":
                members = self.message.new_chat_members
                for member in members:
                    self.member = member
                    self.member_user_id = self.member.id
                    self.member_username = self.member.username
                captcha = True
                if captcha:  # add mongo
                    keybord = [
                        {"text": "Captcha", "callback_data": f"/captcha --type=captcha"}
                    ]
                    await self.__client.send_message(
                        self.message.chat.id,
                        f"@{self.member_username} has joined the Chat !\nSolve the captcha ->",
                        buttons=keybord,
                    )
                else:
                    await self.__client.send_message(
                        self.message.chat.id,
                        f"@{self.member_username} has joined the Chat !",
                    )
            elif str(self.message.service).split(".")[-1] == "LEFT_CHAT_MEMBERS":
                member_username = self.message.left_chat_member.username
                await self.__client.send_message(
                    self.message.chat.id, f"@{member_username} has left the Chat."
                )
            elif str(self.message.service).split(".")[-1] == "PINNED_MESSAGE":
                await self.__client.send_message(
                    self.message.chat.id,
                    f"A new message has been pinned by @{self.username}.\nCheck now !",
                )
        else:
            return
