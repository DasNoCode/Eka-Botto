import os
import importlib.util
from Structures.Client import SuperClient
from Structures.Message import Message
from Helpers.JsonObject import JsonObject


class MessageHandler:

    commands = {}

    def __init__(self, client: SuperClient):
        self.__client = client

    async def handler(self, M: Message):
        contex = JsonObject(self.parse_args(M.message))
        isCommand = M.message.startswith(self.__client.prifix)

        if not isCommand:
            return

        if (M.message == self.__client.prifix):
            return await self.__client.send_message(M.chat_id, f"Enter a command following {self.__client.prifix}")

        cmd = self.commands[contex.cmd] if contex.cmd in self.commands.keys(
        ) else None

        if not cmd:
            return await self.__client.send_message(M.chat_id, "Command does not available!!")
        await cmd.exec(M, contex)

    async def load_commands(self, folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith('.py'):
                module_name = filename[:-3]
                file_path = os.path.join(folder_path, filename)

                spec = importlib.util.spec_from_file_location(
                    module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                class_ = getattr(module, "Command")
                instance = class_(self.__client, self)
                self.commands[instance.config.command] = instance
                aliases = instance.config["aliases"] if hasattr(
                    instance.config, "aliases") else []
                for alias in aliases:
                    self.commands[alias] = instance

    def parse_args(self, raw):
        args = raw.split(' ')
        cmd = args.pop(0).lower()[
            len(self.__client.prifix):] if args else ''
        text = ' '.join(args)
        flags = {}

        for arg in args:
            if arg.startswith('--'):
                key, value = arg[2:].split('=', 1)
                flags[key] = value
            elif arg.startswith('-'):
                flags[arg] = ''
        return {
            'cmd': cmd,
            'text': text,
            'flags': flags,
            'args': args,
            'raw': raw
        }