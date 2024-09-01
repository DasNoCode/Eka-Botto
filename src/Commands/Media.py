from Structures.Command.BaseCommand import BaseCommand
from Helpers.Ytdl import YouTubeDownloader
from Structures.Message import Message
from Ytdl import link


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(client, handler, {
            'command': 'mediadl',
            'category': 'core',
            'description': {
                'content': 'Download Youtube videos and music'
            },
            'exp': 1
        })

    async def exec(self, M: Message, contex):
        print(contex.flags, link)

        ytdl = YouTubeDownloader()
        if contex.flags == 'video':
            title, path, length = ytdl.video_dl(link)
            await self.client.send_video(M.chat_id, path, caption=f"Title: {title}\nDuration: {length}")
            M.urls.pop[0]
        elif contex.flags == 'audio':
            title, path, length = ytdl.audio_dl(link)
            await self.client.send_audio(M.chat_id, path, caption=f"Title: {title}\nDuration: {length}")
            M.urls.pop[0]
