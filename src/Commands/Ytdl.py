from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Structures.Command.BaseCommand import BaseCommand
from Helpers.Ytdl import YouTubeDownloader
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(client, handler, {
            'command': 'ytdl',
            'category': 'core',
            'description': {
                'content': 'Download Youtube videos and music'
            },
            'exp': 1
        })

    async def exec(self, M: Message, contex):
        if not M.urls:
            await self.client.send_message(M.chat_id, "Provide the youtube video link🔗 to download.")
        global link
        link = contex.text
        keybord = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                    "YouTube video 📼", callback_data=f"/mediadl _video")],
                [InlineKeyboardButton(
                    "YouTube Music 🎶", callback_data=f"/mediadl _audio")]
            ])
        await self.client.send_message(M.chat_id, "What you want to download ?", reply_markup=keybord)
