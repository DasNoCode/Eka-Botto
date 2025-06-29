from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message
import re


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "ban",
                "category": "chat",
                "xp": False,
                "AdminOnly": False,
                "OwnerOnly": True,
                "description": {"content": "Ban user from using the bot"},
            },
        )

    async def exec(self, M: Message, context):

        if M.reply_to_message:
            user_name = M.reply_to_message.replied_user.user_name
            user_id = M.reply_to_message.replied_user.user_id
        elif M.mentioned:
            usermentioned_user = M.mentioned[0]
            user_name = usermentioned_user.user_name
            user_id = usermentioned_user.user_id
        else:
            return await self.client.send_message(
                M.chat_id, f"@{M.sender.user_name} mention or replay to an user to ban!"
            )

        if user_id == self.client.bot_id:
            return await self.client.send_message(
                M.chat_id, f"@{M.sender.user_name} oh no! you can't ban me!"
            )

        user_data = self.client.db.User.get_user(user_id=user_id).get("ban")
        if user_data.get("is_ban"):
            return await self.client.send_message(
                M.chat_id, f"@{M.sender.user_name} this user is already **banned!**"
            )

        if context[2]:
            text = context[2].get("reason", "") or ""
            raw_time = context[2].get("time", "")
            search_text = f"{text} {raw_time}"
        else:
            text = context[1]
            for word in ["/ban", f"@{user_name}"]:
                text = text.replace(word, "")
            search_text = text
        time_pattern = re.compile(
            r"(?:time\s*=\s*)?(?P<num>\d+)?\s*(?P<unit>seconds?|minutes?|hours?|days?|weeks?|months?|years?)\b",
            re.IGNORECASE,
        )

        seconds_map = {
            "second": 1,
            "minute": 60,
            "hour": 3600,
            "day": 86400,
            "week": 604800,
            "month": 2592000,
            "year": 31536000,
        }

        time = None
        match = time_pattern.search(search_text)
        if match:
            num = int(match.group("num")) if match.group("num") else 1
            unit = match.group("unit").rstrip("s").lower()
            time = num * seconds_map[unit]
            text = time_pattern.sub("", search_text)

        text = re.sub(r"\btime\b", "", text, flags=re.IGNORECASE)
        text = " ".join(text.split())

        user_data = self.client.db.User.get_user(user_id=user_id).get("ban")
        self.client.db.User.update_user(
            user_id,
            {
                "ban": {
                    "no_of": user_data.get("no_of") + 1,
                    "is_ban": True,
                    "reason": text,
                    "time": time,
                }
            },
        )
        user_data = self.client.db.User.get_user(user_id=user_id).get("ban")
        status = "\n".join(
            [
                "🚫 **Ban Status:** Banned",
                f"   **• Reason:** {user_data.get('reason', '')}",
                f"   **• Since:** {user_data['time']} UTC"
                if user_data.get("time")
                else "   **• Since:**",
                f"   **• Total Bans:** {user_data.get('no_of', 1)}",
            ]
        )
        await self.client.send_message(
            M.chat_id,
            f"Successfully **banned** @{user_name} from using @{M.bot_username}\n\n{status}",
        )
