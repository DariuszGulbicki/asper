from commands.custom_command import CustomCommand
from utils import text_to_speech as tts
import random

class NothingCommand(CustomCommand):
    
    _responses = ["OK", "No problem.", "Sure.", "Yeah.", "Will do."]

    def get_command(self):
        return "nothing"

    def get_description(self):
        return "Confirms that you want to do nothing."

    def get_author(self):
        return "Dariusz Gulbicki"

    def get_version(self):
        return "1.0.0"

    def _random_response(self):
        return self._responses[random.randint(0, len(self._responses) - 1)]

    def execute(self, args):
        tts.read_text(self._random_response())
        return False
