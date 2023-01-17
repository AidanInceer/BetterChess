from dataclasses import dataclass

import yaml
from box import Box
from yaml import SafeLoader


@dataclass
class Config:
    path: str = r"./config/datasets.yaml"

    def set_config_path(self):
        return self.path

    def create_config(self):
        with open(self.path) as f:
            self.conf = Box(yaml.load(f, Loader=SafeLoader))
        return self.conf
