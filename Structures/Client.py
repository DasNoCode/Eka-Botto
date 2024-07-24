from pyromod import Client
from decouple import config

from pyrogram import enums
from pyrogram import Client, filters
from Structures.Message import Message
from pyrogram.handlers import MessageHandler
from Helpers.Utils import Utils


api_id = config("APP_ID", default=None, cast=int)
api_hash = config("API_HASH", default=None)
bot_token = config("BOT_TOKEN", default=None)


class Client(Client):

    def __init__(self, name: str, api_id: int, api_hash: str, bot_token: str, prifix: str, owner_id: int):
        super().__init__(name=name, api_id=api_id, api_hash=api_hash,
                         bot_token=bot_token)
        self.name = name
        self.bot_token = bot_token
        self.prifix = prifix
        self.owner_id = owner_id
        self.utils = Utils()

    async def admincheck(self, message) -> bool:
        isadmin = await message._client.get_chat_member(message.chat.id, message.from_user.id)
        return isadmin.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]


Bot = Client(name='Robotto', api_id=api_id, api_hash=api_hash,
             bot_token=bot_token, prifix="/", owner_id=1152935968)


async def start_command(bot: Bot, msg: Message):  # type: ignore
    # user = await bot.get_users(message.from_user)
    await bot.send_message(msg.chat_id, "await admincheck(message)")


Bot.add_handler(MessageHandler(start_command, filters.command("start")))

Bot.run()
