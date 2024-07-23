from pyromod import Client
from decouple import config
# from Helpers.Utils import Utils
from pyrogram import enums
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler


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
        # self.utils = Utils()


Bot = Client(name='Robotto', api_id=api_id, api_hash=api_hash,
             bot_token=bot_token, prifix="/", owner_id=1152935968)


async def start_command(bot: Bot, message):  # type: ignore
    # user = await bot.get_users(message.from_user)
    await bot.send_message(message.chat.id, message.from_user.id)

Bot.add_handler(MessageHandler(start_command, filters.command("start")))

Bot.run()
