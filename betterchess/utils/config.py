from dataclasses import dataclass

import yaml
from box import Box
from yaml import SafeLoader


@dataclass
class Config:
    """Creates the config base on the specified config filepath."""

    path: str = r"./config/datasets.yaml"

    def set_config_path(self):
        """sets the config file path."""
        return self.path

    def create_config(self) -> Box:
        """Loads the yaml file and creates the `Box` config object.

        Returns:
            conf (Box): config `Box` object.
        """
        with open(self.path) as f:
            self.conf = Box(yaml.load(f, Loader=SafeLoader))
        return self.conf
