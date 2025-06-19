import importlib.util
import math
import os
import random
import re
from datetime import datetime
from Helpers import Utils
from DiscordLevelingCard import RankCard

from Structures.Client import SuperClient
from Structures.Message import Message


class MessageHandler:

    commands = {}
    ranks = [
        (1, "Novice"),
        (5, "Apprentice"),
        (10, "Warrior"),
        (20, "Elite"),
        (30, "Master"),
        (50, "Grandmaster"),
        (75, "Legendary"),
        (100, "Mythic"),
    ]

    def __init__(self, client: SuperClient):
        self.__client = client

    async def handler(self, M: Message):
        context = self.parse_args(M.message)

        if M.message is None:
            return

        isCommand = M.message.startswith(self.__client.prifix)

        mentioned_user = M.mentioned[0] if M.mentioned else None
        mentioned_user_id = getattr(mentioned_user, "user_id", None)
        mentioned_is_afk = (
            self.__client.db.User.get_user(mentioned_user_id).get(
                "afk", {"is_afk": False}
            )
            if mentioned_user_id
            else {"is_afk": False}
        )

        replied_user = getattr(M.reply_to_message, "replied_user", None)
        replied_user_id = replied_user.user_id if replied_user else None
        replied_is_afk = self.__client.db.User.get_user(replied_user_id).get(
            "afk", {"is_afk": False}
        )
        if self.__client.db.User.get_user(M.sender.user_id)["afk"]["is_afk"] is True:
            current_time = datetime.now().time().strftime("%H:%M:%S")
            self.__client.db.User.set_afk(M.sender.user_id, False, None, current_time)
            await self.__client.send_message(
                M.chat_id,
                f"__@{M.sender.user_name} nice to see you again!__",
            )
        if mentioned_is_afk["is_afk"] and replied_is_afk["is_afk"]:
            return await self.__client.send_message(
                M.chat_id,
                f"__@{M.sender.user_name} @{mentioned_user.user_name} is currently offline.\n**Reason** : {mentioned_is_afk.get('afk_reason', 'None')}__",
            )
        if mentioned_is_afk["is_afk"]:
            await self.__client.send_message(
                M.chat_id,
                f"__@{M.sender.user_name} @{mentioned_user.user_name} is currently offline.\n**Reason** : {mentioned_is_afk.get('afk_reason', 'None')}__",
            )
        elif replied_is_afk["is_afk"]:
            await self.__client.send_message(
                M.chat_id,
                f"__@{M.sender.user_name} @{replied_user.user_name} is currently offline.\n**Reason** : {replied_is_afk.get('afk_reason', 'None')}__",
            )
        
        if not isCommand:  
            self.__client.log.info(
                f"[MSG]: From {M.chat_type} by {M.sender.user_name} ({'ADMIN' if M.isAdmin else 'NOT ADMIN'})"
            )
            return
        
        if M.message is self.__client.prifix:
            return await self.__client.send_message(
                M.chat_id, f"__Enter a command following {self.__client.prifix}__"
            )

        cmd = self.commands[context[0]] if context[0] in self.commands.keys() else None

        if not cmd:
            return await self.__client.send_message(
                M.chat_id, "__Command does not available!!__"
            )
        if cmd.config.OwnerOnly:
            if str(M.sender.user_id) != self.__client.owner_id:
                return await self.__client.send_message(
                    M.chat_id, "__This command can only be used by the owner!!__"
                )

        if cmd.config.AdminOnly:
            if not M.isAdmin:
                return await self.__client.send_message(
                    M.chat_id, "__This command can only be used by an admin!!__"
                )

        self.__client.log.info(
            f"[CMD]: {self.__client.prifix}{context[0]} from {M.chat_type} by {M.sender.user_name} "
            f"({'ADMIN' if M.isAdmin else 'NOT ADMIN'})"
        )

        def get_rank(level):
            rank = "Beginner"
            for lvl, title in self.ranks:
                if level >= lvl:
                    rank = title
                else:
                    break
            return rank
        
        print("results:",cmd.config.OwnerOnly)
        result = self.__client.db.User.get_user(M.sender.user_id)
        xp = result["xp"]
        lvl = result["lvl"]
        current_rank = result.get("rank", "Beginner")
        
        # Gain XP
        xp_gained = random.randint(5, 15)
        xp += xp_gained
        
        # Level up every 100 XP (simple logic)
        xp_per_level = 100
        new_lvl = xp // xp_per_level
        
        # Check for level-up
        leveled_up = new_lvl > lvl
        last_lvl = lvl
        lvl = new_lvl
        
        
        # Optional: update rank based on level
        new_rank = get_rank(lvl)
        
        if leveled_up:
            avatar_url = Utils.Utils.img_to_url(
                await self.__client.download_media(
                    M.sender.user_profile_id,
                    file_name=f'downloads/{M.sender.user_profile_id}.jpg',
                    ttl_seconds=120
                )
            )
        
            rankcard_url = (
                f"https://vacefron.nl/api/rankcard"
                f"?username={M.sender.user_name}"
                f"&avatar={avatar_url}"
                f"&level={lvl}"
                f"&rank={get_rank(lvl)}"
                f"&currentxp={xp}"
                f"&nextlevelxp={xp_per_level}"
                f"&previouslevelxp={last_lvl}"
                f"&custombg=https://media.discordapp.net/attachments/1022533781040672839/1026849383104397312/image0.jpg"
                f"&xpcolor=00ffff"
                f"&isboosting=false"
                f"&circleavatar=true"
            )
        
            await self.__client.send_photo(
                M.chat_id,
                photo=rankcard_url,
                caption=f"@{M.sender.user_name} leveled up to level {lvl} ({new_rank})!",
                

            )


        # Update the user's rank if it has changed
        if new_rank != current_rank:
            self.__client.db.User.update_rank(M.sender.user_id, new_rank)
        
        # Update the user's level and xperience in the database
        self.__client.db.User.lvl_garined(M.sender.user_id, xp, last_lvl, lvl)
        
        # Add the chat ID to the bot's database
        self.__client.db.Botdb.add_chat_id_in_chat_id(M.chat_id)
        await cmd.exec(M, context)
    
    def load_commands(self, folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".py"):
                module_name = filename[:-3]
                file_path = os.path.join(folder_path, filename)

                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                class_ = getattr(module, "Command")
                instance = class_(self.__client, self)
                self.commands[instance.config.command] = instance
                self.__client.log.notice(
                    f"Loaded: {instance.config.command} from {file_path}"
                )
                aliases = (
                    instance.config["aliases"]
                    if hasattr(instance.config, "aliases")
                    else []
                )
                for alias in aliases:
                    self.commands[alias] = instance

        self.__client.log.info("Successfully Loaded all the commnads")

    def parse_args(self, raw):
        if raw is not None:
            args = raw.split(" ")
            cmd = args.pop(0).lower()[len(self.__client.prifix) :] if args else ""
            text = " ".join(args)
            flags = {
                flag: (value if value else None)
                for flag, value in re.findall(r"--(\w+)(?:=(\S*))?", raw)
            }

            return (cmd, text, flags, args, raw)
    
    def load_apis():
        pass




