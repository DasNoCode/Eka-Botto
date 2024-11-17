import os
import sys

from decouple import config
from pyrogram import filters
from pyrogram.types import CallbackQuery

from Handler.EventHandler import EventHandler
from Handler.MessageHandler import MessageHandler
from Structures.Client import SuperClient
from Structures.Message import Message

name = config("NAME", default=None)
api_id = config("APP_ID", default=None, cast=int)
api_hash = config("API_HASH", default=None)
bot_token = config("BOT_TOKEN", default=None)
prefix = config("PREFIX", default=None)
owner_id = config("OWNER_ID", default=None)
filepath = config("FILEPATH", default="databse.json")


Bot = SuperClient(
    name=name,
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
    filepath=filepath,
    prefix=prefix,
    owner_id=owner_id,
)

sys.path.insert(0, os.getcwd())
instance = MessageHandler(Bot)
eventInstance = EventHandler(Bot)
instance.load_commands("src/Commands")


@Bot.on_message(
    (
        filters.text
        | filters.reply_keyboard
        | filters.inline_keyboard
        | filters.photo
        | filters.audio
        | filters.voice
        | filters.animation
    ),
    group=-1,
)
async def on_message(client: SuperClient, message: Message):
    await instance.handler(await Message(client, message).build())


@Bot.on_callback_query()
async def on_callback(client: SuperClient, callback: CallbackQuery):
    await instance.handler(await Message(client, callback).build())


@Bot.on_message(filters.service)
async def new_member(client: SuperClient, message: Message):
    await eventInstance.handler(message)


if __name__ == "__main__":
    Bot.log.info("Bot has started!! 🤖")
    Bot.run()
