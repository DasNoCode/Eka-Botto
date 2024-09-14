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
        if not len(M.urls):
            return await self.client.send_message(M.chat_id, "Provide the youtube video link🔗 to download.")
        keys = list(contex[2].keys())

        if len(keys):
            try:
                if keys[0] == "video":
                    print(contex[2])
                    title, path, length = YouTubeDownloader.video_dl(
                        url=contex[2][keys[0]])
                    await self.client.send_video(M.chat_id, path, caption=f"Title: {title}\nDuration: {length}")
                    return YouTubeDownloader.delete()
            except Exception as e:
                return await self.client.send_message(M.chat_id, "Something went wrong !")

            if keys[0] == "audio":
                try:
                    title, path, length = YouTubeDownloader.audio_dl(
                        url=contex[2][keys[0]])
                    await self.client.send_audio(M.chat_id, path, caption=f"Title: {title}\nDuration: {length}")
                    return YouTubeDownloader.delete()
                except Exception as e:
                    return await self.client.send_message(M.chat_id, "Something went wrong !")

        keybord = [{
            "text": "YouTube video 📼",
            "callback_data": f"/ytdl --video={M.urls[0]}"
        }, {
            "text": "YouTube Music 🎶",
            "callback_data": f"/ytdl --audio={M.urls[0]}"
        }
        ]
        await self.client.send_message(M.chat_id, "What you want to download ?", buttons=keybord)
