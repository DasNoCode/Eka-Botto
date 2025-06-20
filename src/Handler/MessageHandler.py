import importlib.util
import os
import random
import re
from datetime import datetime
from Helpers import Utils
from Structures.Client import SuperClient
from Structures.Message import Message


class MessageHandler:

    commands = {}

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

        def get_user_rank(user_id, all_users):
            sorted_users = sorted(all_users, key=lambda x: x["xp"], reverse=True)
        
            for index, user in enumerate(sorted_users, start=1):
                if user["user_id"] == user_id:
                    return index
            return -1  # If not found
        
        
        if cmd.config.xp:
            result = self.__client.db.User.get_user(M.sender.user_id)
            xp = result["xp"]
            lvl = result["lvl"]
        
            xp_gained = random.randint(5, 15)
            xp += xp_gained
        
            xp_per_level = 5 * (lvl ** 2) + 50
            last_lvl = lvl
            leveled_up = False
        
            if xp >= xp_per_level:
                xp -= xp_per_level
                lvl += 1
                leveled_up = True
        
            self.__client.db.User.update_user(M.sender.user_id, {"xp": xp, "lvl": lvl})
        
            rank = get_user_rank(M.sender.user_id, self.__client.db.User.get_all_users())
            self.__client.db.User.update_user(M.sender.user_id, {"rank": rank})

            if leveled_up:
                avatar_url = Utils.Utils.img_to_url(
                    await self.__client.download_media(
                        M.sender.user_profile_id,
                        file_name=f'Images/{M.sender.user_profile_id}.jpg'
                    )
                )
        
                rankcard_url = (
                    "https://vacefron.nl/api/rankcard"
                    f"?username={M.sender.user_name}"
                    f"&avatar={avatar_url}"
                    f"&level={lvl}"
                    f"&rank={rank}"
                    f"&currentxp={xp}"
                    f"&nextlevelxp={5 * (lvl ** 2) + 50}"
                    f"&previouslevelxp={xp_per_level}"
                    f"&custombg=https://media.discordapp.net/attachments/1022533781040672839/1026849383104397312/image0.jpg"
                    f"&xpcolor=00ffff"
                    f"&isboosting=false"
                    f"&circleavatar=true"
                )
        
                await self.__client.send_photo(
                    M.chat_id,
                    rankcard_url,
                    caption=f"@{M.sender.user_name} leveled up to level {lvl} #{rank}!"
                )
                self.__client.db.User.update_user(M.sender.user_id, {"rank": rank}) 
                self.__client.db.User.lvl_garined(M.sender.user_id, xp, last_lvl, lvl)
        
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




