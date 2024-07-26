from pyromod import Client
from pyrogram import enums
from decouple import config
from Helpers.Utils import Utils


name = config("NAME", default=None)
api_id = config("APP_ID", default=None, cast=int)
api_hash = config("API_HASH", default=None)
bot_token = config("BOT_TOKEN", default=None)


class Client(Client):
    def __init__(self, name: str, api_id: int, api_hash: str, bot_token: str):
        super().__init__(name=name, api_id=api_id, api_hash=api_hash,
                         bot_token=bot_token)
        self.prifix = "/"
        self.utils = Utils()

    async def admincheck(self, message):
        isadmin = await self.get_chat_member(message.chat.id, message.from_user.id)
        return isadmin.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]


Bot = Client(name=name, api_id=api_id, api_hash=api_hash,
             bot_token=bot_token)
