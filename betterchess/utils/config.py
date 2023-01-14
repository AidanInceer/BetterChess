import yaml
from yaml import SafeLoader

from betterchess.utils.handlers import FileHandler


class Config:
    @staticmethod
    def create_config(path_handler: FileHandler):
        with open(path_handler.config_path) as f:
            config = yaml.load(f, Loader=SafeLoader)
        return config
