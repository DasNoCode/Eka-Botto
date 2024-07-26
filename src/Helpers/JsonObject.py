class JsonObject:
    def __init__(self, config):
        for key, value in config.items():
            if isinstance(value, dict):
                value = JsonObject(value)
            setattr(self, key, value)
