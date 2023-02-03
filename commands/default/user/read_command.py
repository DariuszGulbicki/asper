from commands.custom_command import CustomCommand
from utils import text_to_speech as tts

class ReadCommand(CustomCommand):
    
    def get_command(self):
        return "read"

    def get_description(self):
        return "Reads the text you provide."

    def get_author(self):
        return "Dariusz Gulbicki"

    def get_version(self):
        return "1.0.0"

    def execute(self, args):
        tts.read_text(args)
        return False