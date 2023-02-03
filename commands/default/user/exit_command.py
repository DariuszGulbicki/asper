from commands.custom_command import CustomCommand
from utils import audio_effects as audio
import sys

class ExitCommand(CustomCommand):
    
    def get_command(self):
        return "exit"

    def get_description(self):
        return "Exits the program."

    def get_author(self):
        return "Dariusz Gulbicki"

    def get_version(self):
        return "1.0.0"

    def execute(self, args):
        audio.play_system_stopped()
        sys.exit()