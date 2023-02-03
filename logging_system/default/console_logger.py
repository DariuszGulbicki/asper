from logging_system.logger_levels import LoggerLevels as Level
from logging_system.log_handler import LogHandler

from utils.template_engine import Template
from datetime import datetime

class ConsoleLogger(LogHandler):

    _template = None

    def get_id(self):
        return "console"

    def get_name(self):
        return "Console Logger (default)"

    def get_description(self):
        return "Logs messages to the console"

    def get_author(self):
        return "Dariusz Gulbicki"

    def get_version(self):
        return "1.0.0"

    def set_config(self, config):
        super().set_config(config)
        try:
            self._template = Template(config["logging_format"])
        except KeyError:
            self._template = Template("{level_prefix} {origin} {message} {cause} {time}")
        self._template.set_placeholder_headers(["level_prefix", "origin", "message", "cause", "time"])

    def _process_time(self, format):
        return "(" + datetime.now().strftime(format) + ")"

    def _process_level(self, level):
        if level == Level.DEBUG:
            return "[DEBUG]"
        elif level == Level.INFO:
            return "[INFO]"
        elif level == Level.WARNING:
            return "[WARNING]"
        elif level == Level.ERROR:
            return "[ERROR]"
        elif level == Level.CRITICAL:
            return "[FATAL]"
        else:
            return ""

    def _process_origin(self, origin):
        if origin is None:
            return ""
        else:
            return origin + ":"

    def _process_cause(self, cause):
        if cause is None:
            return ""
        else:
            return str(cause)

    def handle(self, level, message, origin, cause):
        print(self._template.render([self._process_level(level), self._process_origin(origin), message, self._process_cause(cause), self._process_time("%H:%M:%S")]))