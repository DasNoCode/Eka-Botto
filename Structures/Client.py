from pyromod import Client
from decouple import config
# from Helpers.Utils import Utils
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler


api_id = config("APP_ID", default=None, cast=int)
api_hash = config("API_HASH", default=None)
bot_token = config("BOT_TOKEN", default=None)


class Bot(Client):

    def __init__(self, name: str, api_id: int, api_hash: str, bot_token: str):
        super().__init__(name=name, api_id=api_id, api_hash=api_hash,
                         bot_token=bot_token)
        # self.utils = Utils()


bot = Bot(name='Robotto', api_id=api_id, api_hash=api_hash,
          bot_token=bot_token)


async def start_command(bot, message):
    await bot.send_message(message.chat.id, message.chat["enities"]["type"])

bot.add_handler(MessageHandler(start_command, filters.command("start")))

bot.run()
