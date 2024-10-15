from Helpers.JsonObject import JsonObject
from Structures.Client import SuperClient


class BaseCommand:
    def __init__(self, client: SuperClient, handler, config):
        self.client = client
        self.handler = handler
        self.config = JsonObject(config)

    async def exec(self, msg, arg):
        raise NotImplementedError("Exec function must be declared in subclasses")
