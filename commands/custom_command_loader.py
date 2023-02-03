from importlib import import_module
from importlib.machinery import SourceFileLoader
import os

from logging_system import logger
from commands.custom_command import CustomCommand
from utils import responder as res
from utils import printer
from utils import path_utils as paths

_user_disabled_commands = []
_assistant_disabled_commands = []

_user_commands = []
_assistant_commands = []

def _load_commands_from_directory(dir):
    temp_commands = []
    for file in os.listdir(dir):
        if file.endswith(".py"):
            logger.debug("Loading command from file " + file, "Command loader")
            module = SourceFileLoader(file[:-3], os.path.join(dir, file)).load_module()
            for name, obj in module.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, CustomCommand):
                    temp_commands.append(obj())
    return temp_commands


def _load_default_user_commands():
    logger.debug("Loading default user commands", "Command loader")
    _user_commands.extend(_load_commands_from_directory(paths.get_installed_path("commands/default/user/")))

def _load_default_assistant_commands():
    logger.debug("Loading default assistant commands", "Command loader")
    _assistant_commands.extend(_load_commands_from_directory(paths.get_installed_path("commands/default/assistant/")))

def _load_custom_user_commands():
    try:
        logger.debug("Loading custom user commands", "Command loader")
        _user_commands.extend(_load_commands_from_directory(os.path.join(paths.get_default_app_folder() + "/user_commands/")))
    except FileNotFoundError:
        logger.warn("Asper custom user commands directory not found.")

def _load_custom_assistant_commands():
    try:
        logger.debug("Loading custom assistant commands", "Command loader")
        _assistant_commands.extend(_load_commands_from_directory(os.path.join(paths.get_default_app_folder() + "/assistant_commands/")))
    except FileNotFoundError:
        logger.warn("Asper custom assistant commands directory not found.")

def _cache_commands():
    global _user_commands
    global _assistant_commands
    logger.debug("Caching commands", "Command loader")
    _user_commands = []
    _assistant_commands = []
    _load_default_user_commands()
    _load_default_assistant_commands()
    _load_custom_user_commands()
    _load_custom_assistant_commands()

def _add_user_commands():
    logger.debug("Adding user commands", "Command loader")
    for command in _user_commands:
        if command.get_command() not in _user_disabled_commands and command.get_command() != None:
            logger.debug("Registering user command " + command.get_command(), "Command loader")
            res.register_user_command(command.get_command(), command.execute)

def _add_assistant_commands():
    logger.debug("Adding assistant commands", "Command loader")
    for command in _assistant_commands:
        if command.get_command() not in _assistant_disabled_commands and command.get_command() != None:
            logger.debug("Registering assistant command " + command.get_command(), "Command loader")
            res.register_assistant_command(command.get_command(), command.execute)

def load_commands():
    logger.debug("Loading commands", "Command loader")
    _cache_commands()
    _add_user_commands()
    _add_assistant_commands()

def pretty_print_disabled_user_commands():
    printer.pretty_print_list_vertical(_user_disabled_commands)

def pretty_print_disabled_assistant_commands():
    print(_assistant_disabled_commands)
    printer.pretty_print_list_vertical(_assistant_disabled_commands)

def pretty_print_user_commands():
    table = []
    for command in _user_commands:
        table.append([command.get_command(), command.get_description(), command.get_author(), command.get_version()])
    printer.pretty_print_table(table, ["Name", "Description", "Author", "Version"])

def pretty_print_assistant_commands():
    table = []
    for command in _assistant_commands:
        table.append([command.get_command(), command.get_description(), command.get_author(), command.get_version()])
    printer.pretty_print_table(table, ["Name", "Description", "Author", "Version"])