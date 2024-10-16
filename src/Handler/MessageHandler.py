import importlib.util
import os
import re

from Structures.Client import SuperClient
from Structures.Message import Message


class MessageHandler:

    commands = {}

    def __init__(self, client: SuperClient):
        self.__client = client

    async def handler(self, M: Message):
        contex = self.parse_args(M.message)

        if M.message is None:
            return

        isCommand = M.message.startswith(self.__client.prifix)

        if not isCommand:
            self.__client.log.info(
                f"[MSG]: From {M.chat_type} by {M.sender.user_name}({"ADMIN" if M.isAdmin else "NOT ADMIN"})"
            )
            return

        if M.message is self.__client.prifix:
            return await self.__client.send_message(
                M.chat_id, f"Enter a command following {self.__client.prifix}"
            )

        cmd = self.commands[contex[0]] if contex[0] in self.commands.keys() else None

        if not cmd:
            return await self.__client.send_message(
                M.chat_id, "Command does not available!!"
            )

        self.__client.log.info(
            f"[CMD]: {self.__client.prifix}{contex[0]} from {M.chat_type} by {M.sender.user_name}({"ADMIN" if M.isAdmin else "NOT ADMIN"})"
        )
        try:
            await cmd.exec(M, contex)
        except Exception as e:
            self.__client.log.error(str(e))

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
