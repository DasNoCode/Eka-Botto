from Structures.Client import Bot
from src.Helpers.DynamicConfig import DynamicConfig


class BaseCommand:
    def __init__(self, client: Bot, handler, config):
        self.client = client
        self.handler = handler
        self.config = DynamicConfig(config)

    async def exec(self, msg, arg):
        # raise "Exec Function must be decleared"
        raise NotImplementedError(
            "Exec function must be declared in subclasses")
