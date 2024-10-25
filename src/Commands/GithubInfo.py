import aiohttp

from Structures.Command.BaseCommand import BaseCommand
from Structures.Message import Message


class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "git",
                "category": "core",
                "description": {"content": "Get GitHub user information"},
                "exp": 1,
            },
        )

    async def exec(self, M: Message, context):
        if len(M.message.split()) == 1:
            await self.client.send_message(M.chat_id, "Usage: `git (username)`")
            return

        username = M.message.split(None, 1)[1]
        URL = f"https://api.github.com/users/{username}"

        async with aiohttp.ClientSession() as session:
            async with session.get(URL) as request:
                if request.status == 404:
                    return await self.client.send_message(
                        M.chat_id, f"`{M.sender.user_name} not found`"
                    )

                result = await request.json()

                url = result.get("html_url", None)
                name = result.get("name", None)
                company = result.get("company", None)
                bio = result.get("bio", None)
                created_at = result.get("created_at", "Not Found")

                REPLY = (
                    f"**GitHub Info for `{username}`**"
                    f"\n**Username:** `{name}`\n**Bio:** `{bio}`\n**URL:** {url}"
                    f"\n**Company:** `{company}`\n**Created at:** `{created_at}`"
                )

                if not result.get("repos_url", None):
                    return await self.client.send_message(M.chat_id, REPLY)

                async with session.get(result.get("repos_url", None)) as request:
                    if request.status == 404:
                        return await self.client.send_message(M.chat_id, REPLY)

                    repos = await request.json()
                    REPLY += "\n**Repos:**\n"

                    for repo in repos:
                        REPLY += f"[{repo.get('name')}]({repo.get('html_url')})\n"

                    await self.client.send_message(M.chat_id, REPLY)
