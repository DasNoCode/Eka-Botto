import os
import sys

from decouple import config
from pyrogram import filters
from pyrogram.types import CallbackQuery

from Handler.EventHandler import EventHandler
from Handler.MessageHandler import MessageHandler
from Structures.Client import SuperClient
from Structures.Message import Message

bot_name = config("BOT_NAME", default=None)
api_id = config("APP_ID", default=None, cast=int)
api_hash = config("API_HASH", default=None)
bot_token = config("BOT_TOKEN", default=None)
prefix = config("PREFIX", default=None)
owner_id = config("OWNER_ID", default=None, cast=int)
bot_id = config("BOT_ID", default=None, cast=int)
user_db_filepath = config("USER_DB_FILEPATH", default="UserDatabse.json")
chat_db_filepath = config("CHAT_DB_FILEPATH", default="ChatDatabse.json")
bot_name_ASCII = config("BOT_NAME_ASCII", default="Bot is Online!")



Bot = SuperClient(
    name=bot_name,
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
    user_db_filepath=user_db_filepath,
    chat_db_filepath=chat_db_filepath,
    prefix=prefix,
    owner_id=owner_id,
    bot_id=bot_id

)

sys.path.insert(0, os.getcwd())
instance = MessageHandler(Bot)
eventInstance = EventHandler(Bot)
instance.loadCommands("src/Commands")


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
    Bot.log.info(bot_name_ASCII)
    Bot.run()
