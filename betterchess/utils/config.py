import yaml
from box import Box
from yaml import SafeLoader


class Config:
    def set_config_path(self):
        self.path = r"./config/datasets.yaml"
        return self.path

    def create_config(self):
        with open(r"./config/datasets.yaml") as f:
            self.config = Box(yaml.load(f, Loader=SafeLoader))
        return self.config
