from pyromod import Client
from decouple import config
from pyrogram.utils import *

api_id = config("APP_ID", default=None, cast=int)
api_hash = config("API_HASH", default=None)
bot_token = config("BOT_TOKEN", default=None)


class Bot(Client):

    def __init__(self, name: str, api_id: int, api_hash: str, bot_token: str, plugins: str):
        super().__init__(name=name, api_id=api_id, api_hash=api_hash,
                         bot_token=bot_token, plugins=dict(root=plugins))


bot = Bot(name='Robotto', api_id=api_id, api_hash=api_hash,
          bot_token=bot_token, plugins="plugins")

bot.run()
