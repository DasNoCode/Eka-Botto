from Structures.Client import Bot


class Message:

    urls = []

    numbers = []

    mentioned = []

    def __init__(self, client: Bot, message):  # type: ignore
        self.__M = message
        self.Info = self.__M.chat
        self.message = self.__M.text
        self.__client = client
        user_id = self.__M.from_user.id
        self.sender = {
            "user_id": user_id,
            "user_name": self.__M.from_user.username
        }
        self.chat = "SUPERGROUP" if str(message.chat.type)[
            len("ChatType."):].strip() else "PRIVATE"
        self.chatid = self.Info.id
        self.type = str(message.chat.type)[
            len("MessageMediaType."):].strip()
        self.content = message.text

        if message.entities[1].type[len("MessageEntityType."):].strip() == "MENTION":
            for mention in [mention for mention in self.__M.command[1:] if mention.startswith('@')]:
                self.mentioned.append({
                    "user_id": self.__client.get_users(mention).id,
                    "user_name": self.__client.get_users(mention).id.username
                })
        elif (self.Message.extendedTextMessage.contextInfo.participant):
            self.mentioned.append({
                "jid": self.__client.build_jid(self.Message.extendedTextMessage.contextInfo.participant).User,
                "username": self.__client.contact.get_contact(self.__client.build_jid(self.Message.extendedTextMessage.contextInfo.participant)).PushName
            })

    def build(self):
        for url in self.__client.utils.get_urls(self.content):
            self.urls.append(url)

        for number in self.__client.utils.extract_numbers(self.content):
            self.numbers.append(number)

        self.group = self.__client.get_group_info(self.gcjid)
        self.isAdmin = self.sender['jid'] in self.__client.filter_admin_users(
            self.group.Participants)
        return self

    def raw(self):
        return self.__M
