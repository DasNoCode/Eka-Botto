import sys
import os
from Structures.Client import SuperClient
from Handler.MessageHandler import MessageHandler
from Handler.EventHandler import EventHandler
from pyrogram.types import CallbackQuery
from Structures.Message import Message
#from decouple import config
from pyrogram import filters


#name = config("NAME", default=None)
#api_id = config("APP_ID", default=None, cast=int)
#api_hash = config("API_HASH", default=None)
#bot_token = config("BOT_TOKEN", default=None)
#prefix = config("PREFIX", default=None)

name="Robotto-Bot"
api_id=28359218
api_hash='7b00b1e0f2abd35cd81bdfe931570b50'
bot_token='6230570474:AAEflQDABK76jpGcr0JM3dow6YjPjBI1Vy8'
prefix="/"

Bot = SuperClient(name=name, api_id=api_id, api_hash=api_hash,
                  bot_token=bot_token, prefix=prefix)

sys.path.insert(0, os.getcwd())
instance = MessageHandler(Bot)
eventInstance = EventHandler(Bot)
instance.load_commands("src/Commands")


@Bot.on_message(filters.all, group=-1)
async def on_message(client: SuperClient, message: Message):
    await instance.handler(await Message(client, message).build())


@Bot.on_callback_query()
async def on_callback(client: SuperClient, callback: CallbackQuery):
    callback.data = Bot.callback_data_map[callback.data]
    await instance.handler(await Message(client, callback).build())


@Bot.on_message(filters.service)
async def new_member(client: SuperClient, message: Message):
    await eventInstance.handler(message)

Bot.run()
