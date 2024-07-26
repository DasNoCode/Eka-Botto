class DynamicConfig:
    def __init__(self, config):
        for key, value in config.items():
            if isinstance(value, dict):
                value = DynamicConfig(value)
            setattr(self, key, value)
