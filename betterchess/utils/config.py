import yaml
from box import Box
from yaml import SafeLoader


class Config:
    def __init__(self) -> None:
        self.config_path = self.set_config_path()
        self.conf = self.create_config()

    def set_config_path(self):
        return r"./config/datasets.yaml"

    def create_config(self):
        with open(self.config_path) as f:
            config = Box(yaml.load(f, Loader=SafeLoader))
        return config
