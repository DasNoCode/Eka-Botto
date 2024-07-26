from pyromod import Client
from pyrogram import enums
from Helpers.Utils import Utils


class SuperClient(Client):
    def __init__(self, name: str, api_id: int, api_hash: str, bot_token: str, prefix: str):
        super().__init__(name=name, api_id=api_id, api_hash=api_hash,
                         bot_token=bot_token)
        self.prifix = prefix
        self.utils = Utils()

    async def admincheck(self, message):
        isadmin = await self.get_chat_member(message.chat.id, message.from_user.id)
        return isadmin.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]
