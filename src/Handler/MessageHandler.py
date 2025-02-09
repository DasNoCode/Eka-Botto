import importlib.util
import math
import os
import random
import re
from datetime import datetime

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
                f"__@{M.sender.user_name} @{mentioned_user.user_name}, @{replied_user.user_name} are currently offline \n* @{replied_user.user_name}'s Reason* : {replied_is_afk["afk_reason"]}\n@{mentioned_user.user_name}'s Reason* : {mentioned_is_afk["afk_reason"]}__",
            )
        if mentioned_is_afk["is_afk"]:
            await self.__client.send_message(
                M.chat_id,
                f"__@{M.sender.user_name} @{mentioned_user.user_name} is currently offline.\n**Reason** : {mentioned_is_afk.get("afk_reason", "None")}__",
            )
        elif replied_is_afk["is_afk"]:
            await self.__client.send_message(
                M.chat_id,
                f"__@{M.sender.user_name} @{replied_user.user_name} is currently offline.\n**Reason** : {replied_is_afk.get("afk_reason", "None")}__",
            )

        if not isCommand:
            self.__client.log.info(
                f"[MSG]: From {M.chat_type} by {M.sender.user_name}({"ADMIN" if M.isAdmin else "NOT ADMIN"})"
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
            for lvl, title in ranks:
                if level >= lvl:
                    rank = title
                else:
                    break
            return rank
        
        # Assuming `client`, `M`, and `vac_api` are defined elsewhere in your code
        result = client.db.User.get_user(M.sender.user_id)
        exp = result["exp"]
        lvl = result["lvl"]
        last_lvl = result["last-lvl"]
        current_rank = result.get("rank", "Beginner")
        
        exp_gained = random.randint(1, 10)
        exp += exp_gained
        lvl = 0.1 * (math.sqrt(exp))
        
        new_rank = get_rank(int(lvl))
        
        # Create a rank card using DiscordLevelingCard
        rank_card = RankCard(
            username=M.sender.user_name,
            avatar_url=M.sender.avatar_url,
            current_xp=exp,
            next_level_xp=int((lvl + 1) ** 2 * 10),
            previous_level_xp=int(lvl ** 2 * 10),
            level=int(lvl),
            rank=result.get("rank_position", 1)
        )
        
        # Generate the rank card image
        card = await rank_card.generate()
        
        # Send the level-up message with the rank card
        await client.send_message(M.chat_id, f"@{M.sender.user_name} has leveled up to level {int(lvl)} ({new_rank})!", file=card)
        
        # Update the user's rank if it has changed
        if new_rank != current_rank:
            client.db.User.update_rank(M.sender.user_id, new_rank)
        
        # Update the user's level and experience in the database
        client.db.User.lvl_garined(M.sender.user_id, exp, last_lvl, lvl)
        
        # Add the chat ID to the bot's database
        client.db.Botdb.add_chat_id_in_chat_id(M.chat_id)
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
