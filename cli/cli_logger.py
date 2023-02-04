import click
from termcolor import colored
from config import config_manager as configs
from logging_system import logger as logs
from utils.initializer import init_asper

_render_emojis = True
_render_colors = True

def _render_emoji(emoji):
    if _render_emojis:
        return emoji
    else:
        return ""

def _render_colored(list):
    text = ""
    for item in list:
        if isinstance(item, str):
            text += item + " "
        elif isinstance(item, tuple) and _render_colors:
            text += colored(item[0], item[1]) + " "
        elif isinstance(item, tuple):
            text += item[0] + " "
    return text

@click.group("logger")
def logger():
    """Lets you manage loggers for ASPER system."""
    init_asper()

@click.command("list")
def list():
    """Lists all loaded loggers."""
    click.echo(_render_emoji("📝 ") + _render_colored([("Loaded loggers:", "green")]))
    logs.pretty_print_loaded_handlers()

@click.command("list-active")
def list_enabled():
    """Lists all enabled loggers."""
    click.echo(_render_emoji("📝 ") + _render_colored([("Active loggers:", "green")]))
    logs.pretty_print_active_handlers()

@click.command("enabled")
@click.option("--add", "-a", multiple=True, help="Enables a logger.", type=str)
@click.option("--remove", "-r", multiple=True, help="Disables a logger.", type=str)
def enabled(add, remove):
    """Lists or manages enabled loggers."""
    for handler in add:
        logs.enable_handler(handler)
        configs.config.enabled_loggers.append(handler)
        click.echo(_render_emoji("➕ ") + _render_colored([("Enabled logger:", "green"), (handler, "magenta")]))
    for handler in remove:
        logs.disable_handler(handler)
        configs.config.enabled_loggers.remove(handler)
        click.echo(_render_emoji("➖ ") + _render_colored([("Disabled logger:", "red"), (handler, "magenta")]))
    configs.save()
    click.echo(_render_emoji("📝 ") + _render_colored([("Enabled loggers:", "green")]))
    logs.pretty_print_enabled_handlers()

@click.command("level")
@click.argument("level", required=False, type=str)
def level(level):
    """Shows or sets log level."""
    if level is not None:
        try:
            level = int(level)
        except ValueError:
            if level == "text":
                level = 0
            elif level == "debug":
                level = 1
            elif level == "info":
                level = 2
            elif level == "warning" or level == "warn":
                level = 3
            elif level == "error":
                level = 4
            elif level == "critical":
                level = 5
            else:
                click.echo(_render_emoji("❌ ") + _render_colored([("Invalid log level:", "red"), (level, "magenta")]))
                return
        logs.set_level(level)
        configs.config.logging_level = level
        configs.save()
        click.echo(_render_emoji("🔄 ") + _render_colored([("Log level set to:", "green"), (level, "magenta")]))
    else:
        click.echo(_render_emoji("📝 ") + _render_colored([("Current log level:", "green"), (configs.config.logging_level, "magenta")]))

@click.command("config")
@click.argument("logger", required=True, type=str)
@click.option("--add", "-a", help="Adds a config option.", type=str)
@click.option("--value", "-v", help="Value to add with --add.", type=str)
@click.option("--remove", "-r", help="Removes a config option.", type=str)
def config(logger, add, value, remove):
    """Lists or manages logger config."""
    if logger not in configs.config.loggers_config:
        click.echo(_render_emoji("❌ ") + _render_colored([("Invalid logger:", "red"), (logger, "magenta")]))
        return
    if add is not None:
        if value is None:
            click.echo(_render_emoji("❌ ") + _render_colored([("Please provide a value for the config option:", "red"), (add, "magenta")]))
            return
        configs.config.loggers_config[logger][add] = value
        configs.save()
        click.echo(_render_emoji("➕ ") + _render_colored([("Added config option:", "green"), (add, "magenta"), ("to logger:", "green"), (logger, "magenta")]))
    elif remove is not None:
        if remove not in configs.config.loggers_config[logger]:
            click.echo(_render_emoji("❌ ") + _render_colored([("Invalid config option:", "red"), (remove, "magenta"), ("for logger:", "red"), (logger, "magenta")]))
            return
        configs.config.loggers_config[logger].pop(remove)
        configs.save()
        click.echo(_render_emoji("➖ ") + _render_colored([("Removed config option:", "red"), (remove, "magenta"), ("from logger:", "red"), (logger, "magenta")]))
    else:
        click.echo(_render_emoji("📝 ") + _render_colored([("Config for logger:", "green"), (logger, "magenta")]))
        for key, value in configs.config.loggers_config[logger].items():
            click.echo(_render_emoji("📝 ") + _render_colored([("  ", "green"), (key, "magenta"), ("=", "green"), (value, "magenta")]))

logger.add_command(list)
logger.add_command(list_enabled)
logger.add_command(enabled)
logger.add_command(level)
logger.add_command(config)