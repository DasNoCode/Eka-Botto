from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "banlist",
                "category": "core",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": False,
                "description": {"content": "Show list of banned users"},
            },
        )

    async def exec(self, M: Message, context):
        users = self.client.db.User.get_all_users()
        banned_users = []
        for user in users:
            ban_info = user.get("ban", {})
            if ban_info.get("is_ban"):
                user_id = user.get("user_id")
                reason = ban_info.get("reason")
                banned_users.append(f"**ID:** {user_id} **|** **Reason:** {reason}")

        count = len(banned_users)
        if count == 0:
            text = "**No users are currently banned.**"
        else:
            text = f"**Total banned users:** {count}\n\n" + "\n".join(banned_users)

        await self.client.send_message(M.chat_id, text)