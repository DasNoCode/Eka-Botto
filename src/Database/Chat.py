from collections.abc import MutableMapping

class Chat:
    def __init__(self, db, query):
        self.__db = db
        self.query = query
        if not self.__db.contains(self.query.chat_datas.exists()):
            self.__db.insert({"chat_datas": []})

    def get_all_chat_datas(self):
        chat_data_list = self.__db.get(self.query.chat_datas.exists())
        return chat_data_list["chat_datas"]

    def add_chat(self, chat_datas):
        chat_datas_list = self.get_all_chat_datas()
        if any(c["chat_id"] == chat_datas["chat_id"] for c in chat_datas_list):
            return

        default_chat_datas = {
            "chat_id": chat_datas.get("chat_id", 0),
            "lvl": chat_datas.get("lvl", 1),
            "last_lvl": chat_datas.get("last_lvl", 1),
            "xp": chat_datas.get("xp", 0),
            "is_bot_admin": chat_datas.get("is_bot_admin", False),
            "chat_rules": chat_datas.get("permissions", {}),
            "settings": {
                "language": chat_datas.get("settings", {}).get("language", "en"),
                "events": chat_datas.get("events", False),
                "captchas": chat_datas.get("captchas", False),
                "welcome_enabled": chat_datas.get("settings", {}).get("welcome_enabled", False),
                "welcome_message": chat_datas.get("settings", {}).get(
                    "welcome_message", f"Welcome to {chat_datas.get('chat_title', '')} user!"
                ),
            },
            "stats": {
                "messages_count": chat_datas.get("stats", {}).get("messages_count", 0),
                "active_users": chat_datas.get("stats", {}).get("active_users", []),
            },
            "moderation": {
                "banned_users": chat_datas.get("moderation", {}).get("banned_users", []),
                "mute_list": chat_datas.get("moderation", {}).get("mute_list", []),
            },
            "BrodCast": True,
        }

        chat_datas_list.append(default_chat_datas)
        self.__db.update({"chat_datas": chat_datas_list}, self.query.chat_datas.exists())

    def get_chat_data(self, chat_id):
        chat_datas_list = self.get_all_chat_datas()
        chat = next((u for u in chat_datas_list if u["chat_id"] == chat_id), None)
        if chat:
            return chat
        else:
            self.add_chat({"chat_id": chat_id})
            return self.get_chat_data(chat_id)

    def update_chat_datas(self, chat_id, updates):
        chat_datas_list = self.get_all_chat_datas()
        chat_datas = self.get_chat_data(chat_id)
        if not chat_datas:
            return

        list_without_thechat = [
            chat_data for chat_data in chat_datas_list if chat_data["chat_id"] != chat_id
        ]

        def recursive_update(d, u):
            for k, v in u.items():
                if isinstance(v, MutableMapping) and k in d:
                    d[k] = recursive_update(d.get(k, {}), v)
                else:
                    d[k] = v
            return d

        list_without_thechat.append(recursive_update(chat_datas, updates))
        self.__db.update({"chat_datas": list_without_thechat}, self.query.chat_datas.exists())

    def lvl_garined(self, chat_id, xp, last_lvl, lvl):
        chat_data = self.get_chat_data(chat_id)
        if not chat_data:
            return
        chat_data["xp"] = xp
        chat_data["last_lvl"] = last_lvl
        chat_data["lvl"] = lvl
        self.update_chat_datas(chat_id, chat_data)