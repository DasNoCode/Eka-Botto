import importlib.util
import os
import re
from datetime import datetime

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
        if hasattr(cmd.config, "exp") and cmd.config.exp:
            self.__client.db.User.add_experience(M.sender.user_id, cmd.config.exp)

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
