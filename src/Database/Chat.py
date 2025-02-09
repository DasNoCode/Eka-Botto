class Chat:
    def __init__(self, db, query):
        self.__db = db
        self.query = query
        if not self.__db.contains(self.query.chat.exists()):
            self.__db.insert(
                {"chat": {"events": [], "captchas": [], "permissions": {}}}
            )

    def get_all_events(self):
        chat = self.__db.get(self.query.chat.exists())
        return chat["chat"]["events"]

    def get_all_captchas(self):
        chat = self.__db.get(self.query.chat.exists())
        return chat["chat"]["captchas"]

    def get_all_chatpermissions(self):
        chat = self.__db.get(self.query.chat.exists())
        return chat["chat"]["permissions"]

    def add_chat_id_in_captcha(self, chat_id):
        captchas = self.get_all_captchas()
        if chat_id not in captchas:
            captchas.append(chat_id)
            self.__db.update(
                {
                    "chat": {
                        "events": self.get_all_events(),
                        "captchas": captchas,
                        "permissions": self.get_all_chatpermissions(),
                    }
                },
                self.query.chat.exists(),
            )

    def remove_chat_id_from_captcha(self, chat_id):
        captchas = self.get_all_captchas()
        if chat_id in captchas:
            captchas.remove(chat_id)
            self.__db.update(
                {
                    "chat": {
                        "events": self.get_all_events(),
                        "captchas": captchas,
                        "permissions": self.get_all_chatpermissions(),
                    }
                },
                self.query.chat.exists(),
            )

    def add_chat_id_in_event(self, chat_id):
        events = self.get_all_events()
        if chat_id not in events:
            events.append(chat_id)
            self.__db.update(
                {
                    "chat": {
                        "events": events,
                        "captchas": self.get_all_captchas(),
                        "permissions": self.get_all_chatpermissions(),
                    }
                },
                self.query.chat.exists(),
            )

    def remove_chat_id_from_events(self, chat_id):
        events = self.get_all_events()
        if chat_id in events:
            events.remove(chat_id)
            self.__db.update(
                {
                    "chat": {
                        "events": events,
                        "captchas": self.get_all_captchas(),
                        "permissions": self.get_all_chatpermissions(),
                    }
                },
                self.query.chat.exists(),
            )

    def add_Chat_permissions(self, chat_id, permissions):
        permissions_dict = (
            permissions.__dict__
            if hasattr(permissions, "__dict__")
            else str(permissions)
        )

        all_permissions = self.get_all_chatpermissions()
        if f"{chat_id}" not in all_permissions:
            all_permissions[chat_id] = permissions_dict
            return self.__db.update(
                {
                    "chat": {
                        "events": self.get_all_events(),
                        "captchas": self.get_all_captchas(),
                        "permissions": all_permissions,
                    }
                },
                self.query.chat.exists(),
            )
        all_permissions[f"{chat_id}"].update(permissions_dict)
