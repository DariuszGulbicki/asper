from importlib import import_module
from importlib.machinery import SourceFileLoader
import os

from logging_system.logger_levels import LoggerLevels as Level
from logging_system.log_handler import LogHandler
from utils import printer
from config import config_manager as configs
from utils import path_utils as paths

_handlers = []
_enabled_handlers = [ "console" ]

_default_level = Level.TEXT

def _load_handlers_from_directory(dir):
    temp_commands = []
    for file in os.listdir(dir):
        if file.endswith(".py"):
            module = SourceFileLoader(file[:-3], os.path.join(dir, file)).load_module()
            for name, obj in module.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, LogHandler):
                    temp_commands.append(obj())
    return temp_commands


def _load_default_handlers():
    _handlers.extend(_load_handlers_from_directory(paths.get_installed_path("logging_system/default/")))

def _load_custom_handlers():
    try:
        _handlers.extend(_load_handlers_from_directory(os.path.join(paths.get_default_app_folder() + "/loggers/")))
    except FileNotFoundError:
        pass

def load_handlers():
    _handlers.clear()
    _load_default_handlers()
    _load_custom_handlers()

def load_enabled_handlers(enabled_handlers):
    _enabled_handlers.clear()
    _enabled_handlers.extend(enabled_handlers)

def init(config):
    for handler in _handlers:
        if handler.get_id() in _enabled_handlers:
            try:
                handler.set_config(config[handler.get_id()])
            except KeyError:
                print("!!! NO CONFIG FOR LOGGER " + handler.get_id() + " !!!")
                handler.set_config({})
            handler.enable()

def log(message, level=_default_level, origin=None, cause=None):
    for handler in _handlers:
        if handler.get_id() in _enabled_handlers:
            handler.log(level, message, origin, cause)

def text(message, origin=None, cause=None):
    log(message, Level.TEXT, origin, cause)

def debug(message, origin=None, cause=None):
    log(message, Level.DEBUG, origin, cause)

def info(message, origin=None, cause=None):
    log(message, Level.INFO, origin, cause)

def warn(message, origin=None, cause=None):
    log(message, Level.WARNING, origin, cause)

def error(message, origin=None, cause=None):
    log(message, Level.ERROR, origin, cause)

def critical(message, origin=None, cause=None):
    log(message, Level.CRITICAL, origin, cause)

def enable_handler(id):
    if id in _enabled_handlers:
        log(Level.INFO, "Handler with ID " + id + " is already enabled.", None)
    else:
        _enabled_handlers.append(id)
        log(Level.INFO, "Handler with ID " + id + " has been enabled.", None)

def disable_handler(id):
    if id in _enabled_handlers:
        _enabled_handlers.remove(id)
        log(Level.INFO, "Handler with ID " + id + " has been disabled.", None)
    else:
        log(Level.INFO, "Handler with ID " + id + " is already disabled.", None)

def set_handler_level(id, level):
    for handler in _handlers:
        if handler.get_id() == id:
            handler.set_level(level)
            log(Level.INFO, "Handler with ID " + id + " has been set to level " + str(level) + ".", None)
            return
    log(Level.INFO, "Handler with ID " + id + " does not exist.", None)

def set_default_level(level):
    global _default_level
    _default_level = level
    log(Level.INFO, "Default level has been set to " + str(level) + ".", None)

def get_default_level():
    return _default_level

def get_enabled_handlers():
    return _enabled_handlers

def get_loaded_handlers():
    return _handlers

def set_level(level):
    for handler in _handlers:
        handler.set_level(level)

def pretty_print_enabled_handlers():
    printer.pretty_print_list_vertical(_enabled_handlers)

def pretty_print_loaded_handlers():
    table = []
    for handler in _handlers:
        table.append([handler.get_id(), handler.get_name(), handler.get_description(), handler.get_author(), handler.get_version()])
    printer.pretty_print_table(table, ["ID", "Name", "Description", "Author", "Version"])

def pretty_print_active_handlers():
    table = []
    for handler in _handlers:
        if handler.get_id() in _enabled_handlers:
            table.append([handler.get_id(), handler.get_name(), handler.get_description(), handler.get_author(), handler.get_version()])
    printer.pretty_print_table(table, ["ID", "Name", "Description", "Author", "Version"])