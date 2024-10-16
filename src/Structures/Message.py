from Helpers.JsonObject import JsonObject
from Structures.Client import SuperClient


class Message:

    media_types_with_caption = {
        "photo",
        "audio",
        "video",
        "document",
        "animation",
        "video_note",
    }
    urls = []
    numbers = []
    mentioned = []

    def __init__(self, client: SuperClient, message_or_callback):  # type: ignore
        self.__client = client
        self.is_callback = "CallbackQuery" in str(type(message_or_callback))

        if self.is_callback:
            self.__m = message_or_callback.message
            self.message_id = self.__m.id
            self.message = message_or_callback.data
            self.query_id = message_or_callback.id
            self.sender = JsonObject(
                {
                    "user_id": message_or_callback.from_user.id,
                    "user_name": message_or_callback.from_user.username,
                }
            )
        else:
            self.__m = message_or_callback
            self.sender = JsonObject(
                {
                    "user_id": self.__m.from_user.id,
                    "user_name": self.__m.from_user.username,
                    "user_profile_id": getattr(
                        self.__m.from_user.photo, "small_file_id", None
                    ),
                }
            )
        self.chat_info = self.__m.chat
        self.reply_to_message = self.__m.reply_to_message
        self.chat_type = (
            "SUPERGROUP"
            if str(self.__m.chat.type)[len("ChatType.") :].strip()
            else "PRIVATE"
        )
        self.chat_id = self.chat_info.id
        self.msg_type = (
            str(self.reply_to_message.media.name).lower()
            if self.reply_to_message and hasattr(self.reply_to_message, "media")
            else (
                str(getattr(self.__m, "media", None).name).lower()
                if getattr(self.__m, "media", None)
                else None
            )
        )
        print(self.msg_type)

        if self.msg_type in self.media_types_with_caption:
            self.message = self.__m.caption
        else:
            self.message = self.__m.text

        if self.msg_type in ["voice", "animation", "audio", "photo", "video"]:
            if self.reply_to_message:
                self.file_id = getattr(
                    getattr(self.reply_to_message, self.msg_type, {}), "file_id", None
                )
                print("Replied message file id : ", self.file_id)
                return
            self.file_id = getattr(
                getattr(self.__m, self.msg_type, {}), "file_id", None
            )
            print("Message file id : ", self.file_id)

        self.mentioned = []

    async def build(self):
        print(self.__m)
        self.urls = self.__client.utils.get_urls(self.message)
        self.numbers = self.__client.utils.extract_numbers(self.message)

        self.isAdmin = await self.__client.admincheck(self.__m)

        if self.__m.entities:
            for entity in self.__m.entities:
                if entity.type == "MENTION":
                    mentions = [
                        mention
                        for mention in self.__m.text.split()
                        if mention.startswith("@")
                    ]
                    for mention in mentions:
                        user = await self.__client.get_users(mention)
                        self.mentioned.append(
                            {"user_id": user.id, "user_name": user.username}
                        )
        elif self.__m.reply_to_message:
            reply_user = self.__m.reply_to_message.from_user
            self.mentioned.append(
                {
                    "user_id": reply_user.id,
                    "user_name": reply_user.username,
                    "user_profile_id": getattr(
                        reply_user.photo.small_file_id, "small_file_id", None
                    ),
                }
            )

        return self

    def raw(self):
        return self.__m
