from Structures.Client import Bot
from Handler.MessageHandler import MessageHandler
from Structures.Message import Message
from pyrogram import filters
import sys
import os


sys.path.insert(0, os.getcwd())
instance = MessageHandler(Bot)


@Bot.on_message(filters.all, group=-1)
async def on_message(client: Bot, message: Message):
    await instance.load_commands("src/Commands")
    await instance.handler(await Message(client, message).build())


Bot.run()
