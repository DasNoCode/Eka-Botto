import os

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "chatprofile",
                "category": "core",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": False,
                "description": {"content": "Show the profile and stats of this chat."},
            }
        )

    async def exec(self, M: Message, context):
        chat_title = M.chat_title


        file_path = f'Images/{M.chat_id}.jpg'
        profile_id = getattr(M.chat_info.photo, "big_file_id", None)

        if profile_id:
            await self.client.download_media(
                profile_id,
                file_name=file_path
            )
            photo_path = f"src/{file_path}"


        chat_data = self.client.db.Chat.get_chat_data(M.chat_id)
        if not chat_data:
            await self.client.send_message(M.chat_id, "No data found for this chat.")
            return

        settings = chat_data.get("settings", {})
        stats = chat_data.get("stats", {})
        moderation = chat_data.get("moderation", {})

        status = (
            f"🏠 **Chat Status**\n\n"
            f"**Title:** {chat_title}\n"
            f"**Chat ID:** `{M.chat_id}`\n"
            f"**Level:** {chat_data.get('lvl', 0)}\n"
            f"**XP:** {chat_data.get('xp', 0)}\n"
            f"**Bot Admin:** {'✅' if chat_data.get('is_bot_admin') else '❌'}\n\n"
            
            f"**Settings:**\n"
            f"  • **Language:** {settings.get('language', 'en')}\n"
            f"  • **Events:** {'✅' if settings.get('events') else '❌'}\n"
            f"  • **Captchas:** {'✅' if settings.get('captchas') else '❌'}\n"
            f"  • **Welcome:** {'✅' if settings.get('welcome_enabled') else '❌'}\n"
            f"  • **Welcome Msg:** {settings.get('welcome_message', 'Not set')}\n\n"
            
            f"**Stats:**\n"
            f"  • **Messages:** {stats.get('messages_count', 0)}\n"
            f"  • **Active Users:** {len(stats.get('active_users', []))}\n\n"
            
            f"**Moderation:**\n"
            f"  • **Banned Users:** {len(moderation.get('banned_users', []))}\n"
            f"  • **Muted Users:** {len(moderation.get('mute_list', []))}\n"
            f"  • **Broadcast:** {'✅' if chat_data.get('BrodCast') else '❌'}"
        )
        if photo_path:
            await self.client.send_photo(
                M.chat_id,
                photo=photo_path,
                caption=status
            )
            os.remove(photo_path)
        else:
            await self.client.send_message(M.chat_id, status)