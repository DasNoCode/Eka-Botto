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
                "category": "utility",
                "AdminOnly": False,
                "OwnerOnly": False,
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
                MAX_REPOS_DISPLAY = 5
                MAX_MESSAGE_LENGTH = 4096

                REPLY = (
                    f"[**GitHub Info 🧑‍💻**]\n"
                    f"• **Username** : `{username}`\n"
                    f"• **Bio** : __{bio}__\n"
                    f"• **URL** : __{url}__\n"
                    f"• **Company** : __{company}__\n"
                    f"• **Created at** : __{created_at}__\n"
                )

                if not result.get("repos_url"):
                    return await self.client.send_message(M.chat_id, REPLY)

                async with session.get(result["repos_url"]) as request:
                    if request.status == 404:
                        return await self.client.send_message(M.chat_id, REPLY)

                    repos = await request.json()
                    if repos:
                        REPLY += "• **Repos** :\n"
                        for repo in repos[:MAX_REPOS_DISPLAY]:
                            repo_info = (
                                f"[{repo.get('name')}]({repo.get('html_url')})\n"
                            )
                            if len(REPLY) + len(repo_info) > MAX_MESSAGE_LENGTH:
                                await self.client.send_message(M.chat_id, REPLY)
                                REPLY = ""
                            REPLY += repo_info

                    if REPLY:
                        await self.client.send_message(M.chat_id, REPLY)
