class Config:

    def __init__(self):
        # MAIN #
        self.version = "0.0.1"
        self.selected_language = "en"
        self.selected_persona = "default.asper"
        # LOGGING #
        self.logging_level = 2
        self.enabled_loggers = [ "console_color" ]
        self.loggers_config = {
            "console_color": {
                "disable_colors": False,
                "time_format": "%H:%M:%S",
                "logging_format": "{level_emoji}   {level_prefix} {origin} {message} {time}",
                "ignore_originless": False,
            }
        }
        # CLI #
        self.cli_colored = True
        self.cli_display_emoji = True