import os
import yaml
import platform

from config.config import Config
from personality import personality_manager as personas
from logging_system import logger
from cli import cli_personas
from utils.path_utils import get_default_app_folder


_config_file_name = "config.yml"

config = Config()

def _execute_load_hooks():
    # Load loggers #
    logger.load_enabled_handlers(config.enabled_loggers)
    logger.load_handlers()
    logger.set_level(config.logging_level)
    logger.init(config.loggers_config)
    # Load personality manager #
    personas.change_personality(config.selected_persona)
    personas.load()
    # Load CLI settings #

def save():
    def_app_folder = get_default_app_folder()
    os.makedirs(def_app_folder, exist_ok=True)
    try:
        with open(os.path.join(def_app_folder, _config_file_name), "x") as f:
            f.write(yaml.dump(config))
    except FileExistsError:
        with open(os.path.join(def_app_folder, _config_file_name), "w") as f:
            f.write(yaml.dump(config))

def load():
    global config
    def_app_folder = get_default_app_folder()
    try:
        with open(os.path.join(def_app_folder, _config_file_name), "r") as f:
            config = yaml.load(f.read(), Loader=yaml.Loader)
    except FileNotFoundError:
        save()
    _execute_load_hooks()