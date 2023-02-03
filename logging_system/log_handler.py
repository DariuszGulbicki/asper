from logging_system.logger_levels import from_int, to_int, LoggerLevels as Level

class LogHandler():

    _enabled = False
    _level = Level.WARNING
    _config = {}

    def get_id(self):
        # This is the id of the handler
        pass

    def get_name(self):
        # This is the name of the handler
        pass

    def get_description(self):
        # This is the description of the handler
        pass

    def get_author(self):
        # This is the author of the handler
        pass

    def get_version(self):
        # This is the version of the handler
        pass

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def set_level(self, level):
        self._level = level

    def is_enabled(self):
        return self._enabled

    def get_level(self):
        return self._level

    def set_config(self, config):
        self._config = config

    def get_config(self):
        return self._config

    def handle(self, level, message, origin, cause):
        # This method is called when the logger wants to log a message
        pass

    def log(self, level, message, origin, cause):
        if self._enabled and to_int(level) >= to_int(self._level):
            self.handle(level, message, origin, cause)
