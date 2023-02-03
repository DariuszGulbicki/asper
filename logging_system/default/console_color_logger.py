from logging_system.logger_levels import LoggerLevels as Level
from logging_system.log_handler import LogHandler

from utils.template_engine import Template
from datetime import datetime
from termcolor import colored

class ConsoleColorLogger(LogHandler):

    _template = None

    def get_id(self):
        return "console_color"

    def get_name(self):
        return "Console Color Logger (default)"

    def get_description(self):
        return "Logs messages to the console with colors"

    def get_author(self):
        return "Dariusz Gulbicki"

    def get_version(self):
        return "1.0.0"

    def set_config(self, config):
        super().set_config(config)
        try:
            self._template = Template(config["logging_format"])
        except KeyError:
            self._template = Template("{level_emoji}   {level_prefix} {origin} {message} {cause} {time}")
        self._template.set_placeholder_headers(["level_emoji", "level_prefix", "origin", "message", "cause", "time"])

    def _process_time(self, format):
        return colored("(" + datetime.now().strftime(format) + ")", color="grey")

    def _process_level_emoji(self, level):
        if level == Level.DEBUG:
            return colored("🐛", color="grey")
        elif level == Level.INFO:
            return colored("ℹ️", color="blue")
        elif level == Level.WARNING:
            return colored("⚠️", color="yellow")
        elif level == Level.ERROR:
            return colored("❌", color="red")
        elif level == Level.CRITICAL:
            return colored("🔥", color="red", attrs=["bold"])
        else:
            return ""

    def _process_level(self, level):
        if level == Level.DEBUG:
            return colored("[DEBUG]", on_color="on_green", color="white")
        elif level == Level.INFO:
            return colored("[INFO]", on_color="on_blue", color="white")
        elif level == Level.WARNING:
            return colored("[WARNING]", on_color="on_yellow", color="white")
        elif level == Level.ERROR:
            return colored("[ERROR]", on_color="on_red", color="white")
        elif level == Level.CRITICAL:
            return colored("[FATAL]", on_color="on_black", color="red", attrs=["bold"])
        else:
            return ""

    def _process_origin(self, origin):
        if origin is None:
            return ""
        else:
            return colored(origin + ":", color="magenta")

    def _process_cause(self, cause):
        if cause is None:
            return ""
        else:
            return colored("{" + str(cause) + "}", color="red")

    def handle(self, level, message, origin, cause):
        print(self._template.render([self._process_level_emoji(level), self._process_level(level), self._process_origin(origin), message, self._process_cause(cause), self._process_time("%H:%M:%S")]))