from Structures.Client import Bot


class Message:

    urls = []

    numbers = []

    mentioned = []

    def __init__(self, client: Bot, message):  # type: ignore
        self.__m = message
        self.message = self.__m.text
        self.__client = client
        user_id = self.__m.from_user.id
        self.sender = {
            "user_id": user_id,
            "user_name": self.__m.from_user.username
        }
        self.chat_info = self.__m.chat
        self.chat_type = "SUPERGROUP" if str(message.chat.type)[
            len("ChatType."):].strip() else "PRIVATE"
        self.chat_id = self.chat_info.id
        self.msg_type = str(message.chat.type)[
            len("MessageMediaType."):].strip()

        if message.entities[1].type[len("MessageEntityType."):].strip() == "MENTION":
            for mention in [mention for mention in self.__m.command[1:] if mention.startswith('@')]:
                self.mentioned.append({
                    "user_id": self.__client.get_users(mention).id,
                    "user_name": self.__client.get_users(mention).id.username
                })
        elif (self.__m.reply_to_message):
            self.mentioned.append({
                "user_id": self.__m.reply_to_message.from_user.id,
                "user_name": self.__m.reply_to_message.from_user.username
            })

    async def build(self):
        for url in self.__client.utils.get_urls(self.message):
            self.urls.append(url)

        for number in self.__client.utils.extract_numbers(self.message):
            self.numbers.append(number)

        self.isAdmin = self.sender['user_id'] in await self.__client.admincheck(
            self.__m)
        return self

    def raw(self):
        return self.__m
