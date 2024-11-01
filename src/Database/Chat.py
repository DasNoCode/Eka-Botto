class Chat:
    def __init__(self, db, query):
        self.__db = db
        self.query = query
        if not self.__db.contains(self.query.chat.exists()):
            self.__db.insert({"chat": {"events": [], "captchas": []}})

    def get_all_events(self):
        chat = self.__db.get(self.query.chat.exists())
        return chat["events"]

    def get_all_captchas(self):
        chat = self.__db.get(self.query.chat.exists())
        return chat["captchas"]

    def add_chat_id_in_captcha(self, chat_id):
        if chat_id in self.chat_data["captcha"]:
            return
        self.chat_data["captcha"].append(chat_id)

    def remove_chat_id_from_captcha(self, chat_id):
        if chat_id not in self.chat_data["captcha"]:
            return
        self.chat_data["captcha"].remove(chat_id)

    def add_chat_id_in_event(self, chat_id):
        if chat_id in self.chat_data["events"]:
            return
        self.chat_data["events"].append(chat_id)

    def remove_chat_id_from_events(self, chat_id):
        if chat_id not in self.chat_data["events"]:
            return
        self.chat_data["events"].remove(chat_id)
