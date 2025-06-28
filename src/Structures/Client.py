from pyrogram import enums
from pyromod import Client
import random
from Helpers.Logger import get_logger
from Helpers.Utils import Utils
from Structures.Database import Database as db


class SuperClient(Client):
    def __init__(
        self,
        name: str,
        api_id: int,
        api_hash: str,
        bot_token: str,
        user_db_filepath: str,
        chat_db_filepath: str,
        prefix: str,
        owner_id: int
    ):
        super().__init__(
            name=name, api_id=api_id, api_hash=api_hash, bot_token=bot_token
        )
        self.prifix = prefix
        self.log = get_logger()
        self.database = user_db_filepath, chat_db_filepath
        self.utils = Utils()
        self.owner_id = owner_id


    @property
    def db(self):
        return db(self.database)

    async def admincheck(self, message):
        if message.chat.type in ("group", "supergroup", "channel"):
            isadmin = await self.get_chat_member(message.chat.id, message.from_user.id)
            return isadmin.status in [
                enums.ChatMemberStatus.OWNER,
                enums.ChatMemberStatus.ADMINISTRATOR,
            ]
        return None
    async def xp_lvl(self, message, xp_gained=None):
        result = self.db.User.get_user(message.sender.user_id)
        xp = result["xp"]
        lvl = result["lvl"]
        if xp_gained is None:
            xp_gained = random.randint(1, 3)
        total_xp = result["xp"] + xp_gained
        last_lvl = lvl
        leveled_up = False

        while total_xp >= (5 * (lvl ** 2) + 50):
            lvl += 1
            leveled_up = True

        previouslevelxp = 5 * ((lvl - 1) ** 2) + 50 if lvl > 0 else 0
        nextlevelxp = 5 * (lvl ** 2) + 50
        currentxp = total_xp

        self.db.User.update_user(message.sender.user_id, {"xp": total_xp, "lvl": lvl})
        rank = self.get_user_rank(message.sender.user_id, self.db.User.get_all_users())
        self.db.User.update_user(message.sender.user_id, {"rank": rank})

        if leveled_up:
            avatar_url = self.utils.img_to_url(
                await self.download_media(
                    message.sender.user_profile_id,
                    file_name=f'Images/{message.sender.user_profile_id}.jpg'
                )
            )
            rankcard_url = (
                "https://vacefron.nl/api/rankcard"
                f"?username={message.sender.user_name}"
                f"&avatar={avatar_url}"
                f"&level={lvl}"
                f"&rank={rank}"
                f"&currentxp={currentxp}"
                f"&nextlevelxp={nextlevelxp}"
                f"&previouslevelxp={previouslevelxp}"
                f"&custombg=https://media.discordapp.net/attachments/1022533781040672839/1026849383104397312/image0.jpg"
                f"&xpcolor=00ffff"
                f"&isboosting=false"
                f"&circleavatar=true"
            )
            await self.send_photo(
                message.chat_id,
                rankcard_url,
                caption=f"@{message.sender.user_name} leveled up to level {lvl} #{rank}!"
            )
            self.db.User.lvl_garined(message.sender.user_id, xp, last_lvl, lvl)

    def get_user_rank(self, user_id, all_users):
        sorted_users = sorted(all_users, key=lambda x: x["xp"], reverse=True)
        for index, user in enumerate(sorted_users, start=1):
            if user["user_id"] == user_id:
                return index
        return -1


    async def get_admins_and_owner(self, chat_id):
        admins_info = []
        owner_info = None
    
        async for member in self.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            user = member.user
            username = user.username if user.username else f"{user.first_name or ''} {user.last_name or ''}".strip()
            if member.status == "creator":
                owner_info = (username, user.id)
            elif member.status == "administrator":
                admins_info.append((username, user.id))
        return owner_info, admins_info

