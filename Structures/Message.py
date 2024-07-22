from Structures.Client import bot


class Message:

    urls = []

    numbers = []

    mentioned = []

    def __init__(self, bot, message):
        self.__M = message
        self.Info = self.__M.chat
        self.message = self.__M.text
        self.__client = bot
        user_id = self.Info.chat.from_user.id
        self.sender = {
            "user_id": user_id,
            "username": self.Info.chat.from_user.username
        }
        self.chat = "SUPERGROUP" if str(message.chat.type)[
            len("ChatType."):].strip() else "PRIVATE"
        self.gcjid = self.Info.id
        self.type = str(message.chat.type)[
            len("MessageMediaType."):].strip()
        self.content = message.text

        if (self.Message.extendedTextMessage.contextInfo.quotedMessage.extendedTextMessage.contextInfo.mentionedJID):
            for mention in self.Message.extendedTextMessage.contextInfo.quotedMessage.extendedTextMessage.contextInfo.mentionedJID:
                self.mentioned.append({
                    "chat_id": self.__client.build_jid(mention).User,
                    "username": self.__client.contact.get_contact(self.__client.build_jid(mention)).PushName
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
