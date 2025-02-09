class Botdb:
    def __init__(self, db, query):
        self.__db = db
        self.query = query

        if not self.__db.contains(self.query.chat.exists()):
            self.__db.insert({"chat": {"Botdb": {"chat_id": []}}})

    def get_all_chat_id(self):
        chat = self.__db.get(self.query.chat.exists()) or {}
        return chat.get("chat", {}).get("Botdb", {}).get("chat_id", [])

    def add_chat_id_in_chat_id(self, chat_id):
        chat_ids = self.get_all_chat_id()
        if chat_id not in chat_ids:
            chat_ids.append(chat_id)
            self.__db.update(
                {"chat": {"Botdb": {"chat_id": chat_ids}}}, self.query.chat.exists()
            )
