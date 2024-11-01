from pyrogram import enums
from pyromod import Client

from Helpers.Logger import get_logger
from Helpers.Utils import Utils
from Structures.Database import Database as db


class SuperClient(Client):
    def __init__(
        self,
        name: str,
        api_id: int,
        api_hash: str,
        bot_token: str,
        filepath: str,
        prefix: str,
        owner_id: int,
    ):
        super().__init__(
            name=name, api_id=api_id, api_hash=api_hash, bot_token=bot_token
        )
        self.prifix = prefix
        self.log = get_logger()
        self.filepath = filepath
        self.utils = Utils()
        self.owner_id = owner_id

    @property
    def db(self):
        return db(self.filepath)

    async def admincheck(self, message):
        isadmin = await self.get_chat_member(message.chat.id, message.from_user.id)
        return isadmin.status in [
            enums.ChatMemberStatus.OWNER,
            enums.ChatMemberStatus.ADMINISTRATOR,
        ]
