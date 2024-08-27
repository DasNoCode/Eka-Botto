from Structures.Client import SuperClient
from Helpers.JsonObject import JsonObject


class Message:

    urls = []
    numbers = []
    mentioned = []

    def __init__(self, client: SuperClient, message_or_callback):  # type: ignore
        self.__client = client
        self.is_callback = "CallbackQuery" in str(type(message_or_callback))

        if self.is_callback:
            self.__m = message_or_callback.message
            self.message = message_or_callback.data
            user_id = message_or_callback.from_user.id
            self.sender = JsonObject({
                "user_id": user_id,
                "user_name": message_or_callback.from_user.username
            })
        else:
            self.__m = message_or_callback
            self.message = self.__m.text
            user_id = self.__m.from_user.id
            self.sender = JsonObject({
                "user_id": user_id,
                "user_name": self.__m.from_user.username
            })

        self.chat_info = self.__m.chat
        self.chat_type = "SUPERGROUP" if str(self.__m.chat.type)[
            len("ChatType."):].strip() else "PRIVATE"
        self.chat_id = self.chat_info.id
        self.msg_type = str(self.__m.chat.type)[
            len("MessageMediaType."):].strip()

        self.mentioned = []

    async def build(self):
        self.urls = self.__client.utils.get_urls(self.message)
        self.numbers = self.__client.utils.extract_numbers(self.message)

        self.isAdmin = await self.__client.admincheck(self.__m)

        if self.__m.entities:
            for entity in self.__m.entities:
                if entity.type == "MENTION":
                    mentions = [
                        mention for mention in self.__m.text.split() if mention.startswith('@')]
                    for mention in mentions:
                        user = await self.__client.get_users(mention)
                        self.mentioned.append({
                            "user_id": user.id,
                            "user_name": user.username
                        })
        elif self.__m.reply_to_message:
            reply_user = self.__m.reply_to_message.from_user
            self.mentioned.append({
                "user_id": reply_user.id,
                "user_name": reply_user.username
            })

        return self

    def raw(self):
        return self.__m
